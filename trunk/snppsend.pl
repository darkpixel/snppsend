#!/usr/bin/perl -w

# snppsend v1.95: a simple program to deliver messages to text pagers
#                 using the SNPP protocol.
# Copyright (C) 2004 Aaron C. de Bruyn <code@darkpixel.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# The latest version of snppsend should always be available
# on my website at http://www.darkpixel.com/
# 
# Some shout-outs
# darklordmaven for hammering away at my scripts, looking
#   for bugs, moral support, and games of Halo 2.
# jeek in #pound-perl.pm on EFNet for his words of wisdom.
#   Though he spoke not more than ten words, he pointed
#   out my total perl noobness.
# Steve Kaylor and Brandon Zehm - their original script
#   inspired this program and I borrowed a chunk of
#   their socket and snpp server communication code.

use strict;
use IO::Socket qw (:DEFAULT :crlf);
use LWP::Simple;
use URI::URL;
use XML::Simple;
use Data::Dumper;

my $globerror = '';

my $homecfg = $ENV{'HOME'};
my $tmpdir = "/tmp";

# Init some variables I will be using throughout the script
my $datain = '';
my %receivers = ();
my %providers = ();

my $config = LoadConfigFromFile("/etc/snppsend.conf");
$| = 1;  # Unbuffer stdout

sub LoadConfigFromFile {
	my $cfgfile = shift;
	if ( -e $cfgfile ) {
		return XMLin($cfgfile, ForceArray => 1);
	}
}

sub LoadConfigFromWeb {
	my $url = shift;
	my $webconfig = get($url);
	if ( !defined $webconfig ) {
		return;
	} else {
		return XMLin($webconfig, ForceArray => 1);
	}
	
}

sub ReceiverValid {
	#stub
	#this function needs to make sure the receiver's provider
	#exists and all information is valid and retrievable.
	#we should also make a function to check if a config file is valid.
}

sub ReceiverExists {
	# ReceiverExists() Params
	# $recvr = Name or alias the receiver.
	# RETURN: xml array of receiver information if exists, undef if not.

	my $lookup = shift;

	foreach my $recv ( keys %{$config->{receiver}} ) {
		# Check to see if they named a receiver exactly
		if ( $lookup eq $recv ) {
			return $config->{receiver}->{$recv};
		}

		# Check to see if they passed an alias
		for ( my $i=0; $i <= $#{$config->{receiver}->{$recv}->{alias}}; $i++ ) {
			if ( $config->{receiver}->{$recv}->{alias}[$i] eq $lookup ) {
				return $config->{receiver}->{$recv};
			}	
		}
	}
	return undef;
}

sub ProviderExists {
	# ProviderExists() Params
	# $provdr = Name of the provider.
	# RETURN: xml array of provider information if exists, undef if not.

	my $lookup = shift;

	foreach my $prov ( keys %{$config->{provider}} ) {
		if ( $lookup eq $prov ) {
			return $config->{provider}->{$prov};
		}
	
	}
	return undef;
}

sub GetProviderIP {
	# GetProviderIP() Params
	# $current = Name of the receiver.
	# RETURN: IP Address in standard 0.0.0.0 format of the provider.

	my $current = shift;
	return ProviderExists(ReceiverExists($current)->{provider}[0])->{address}[0];
}

sub GetProviderPort {
	my $current = shift;
	return ProviderExists(ReceiverExists($current)->{provider}[0])->{port}[0];
}

#sub GetProviderMaxChars {
#	my $current = shift;
#	return $providers{$receivers{"$current"}[0]}[2];
#}

sub GetRecipientNumber {
	my $current = shift;
	return ReceiverExists($current)->{number}[0];
}

sub connectTo {
	my ($server, $port) = @_;
	socket(SERVER, PF_INET, SOCK_STREAM, getprotobyname('tcp')) || block {
		$globerror = "Unable to create socket connection to [$server] on [$port]";
		return 0;
	};
	
	my $inet_aton = inet_aton($server) || block {
		$globerror = "Unable to resolve [$server]";
		return 0;
	};
	
	my $dest = sockaddr_in($port, $inet_aton) || block {
		$globerror = "Unable to create data structure sockaddr_in [$port] [$inet_aton]";
		return 0;
	};

	connect(SERVER, $dest) || block {
		$globerror = "Unable to connect to [$server] on [$port]";
		return 0;
	};

	select(SERVER);
	$| = 1;
	select(STDOUT);
	return 1;
}

sub SNPPChat {
	my ($receiver, $message) = @_;
	my $status = <SERVER>;
	if ( $status !~ /220/i ) {
		$status =~ s/$CRLF//;
		$globerror = "The paging server greeted us with [$status]";
		return 0;
	}
	
	print SERVER "PAGE $receiver$CRLF";
	$status = <SERVER>;
	if ( $status !~ /250/i ) {
		$status =~ s/$CRLF//;
		$globerror = "Receiver [$receiver] was rejected with error [$status]";
		return 0;
	}
	
	print SERVER "MESS $message$CRLF";
	$status = <SERVER>;
	if ( $status !~ /250/i ) {
		$status =~ s/$CRLF//;
		$globerror = "Message entered with error [$status]";
		return 0;
	}
	
	print SERVER "SEND$CRLF";
	$status = <SERVER>;
	if ( $status !~ /250/i ) {
		$status =~ s/$CRLF//;
		$globerror = "Message rejected with error [$status]";
		return 0;
	}
	
	print SERVER "QUIT$CRLF";
	$status = <SERVER>;
	if ( $status !~ /221/i ) {
		$status =~ s/$CRLF//;
		$globerror = "Disconnect failed with error [$status]";
		return 0;
	}
	return 1;
}

# Here is where the program really begins...

my $totalreceivers = 0;  # A count of all valid receivers on the command line...

foreach ( @ARGV ) {
	if ( ReceiverExists($_) ) {
		if ( ProviderExists( ReceiverExists($_)->{provider}[0] ) ) {
			$totalreceivers++;
		} else {
			print "Unable to find provider [";
			print ReceiverExists($_)->{provider}[0];
			print "] for receiver [$_]\n";
		}
	}
}

if ( $totalreceivers > 0 ) {
	my $msgtosend = "";
	while (<STDIN>) {
		chomp;
		$msgtosend = "$msgtosend $_";
	}
	chomp($msgtosend);
	foreach (@ARGV) {
		if (ReceiverExists($_)) {
			print "Paging $_...";
			
			if ( connectTo(GetProviderIP($_), GetProviderPort($_)) ) {
				if ( SNPPChat(GetRecipientNumber($_),$msgtosend) ) {
					print "done!\n";
				} else {
					print "ERROR\n";
					print "SNPPChat: [$globerror]\n";
				}
			} else {
				print "ERROR\n";
				print "ConnectTo: [$globerror]\n";
			}
			close SERVER;
		} else {
			print "Paging $_...UNABLE TO LOCATE\n";
		}
	}
} else {
	print "No recipients!\n";
}
