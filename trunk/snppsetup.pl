#!/usr/bin/perl -w

# snppsetup.pl: add/edit/delete providers and/or receivers to from
#               your snppsend configuration file.
# Copyright (C) 2004 - 2005 Aaron C. de Bruyn <code@darkpixel.com>
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

use strict;
use LWP::Simple;
use URI::URL;
use XML::Simple;
use Data::Dumper;
use Curses::UI;

my $cui = new Curses::UI( -color_support=> 1 );
$cui->status('Welcome to snppsetup');
sleep 1;
$cui->nostatus;

my @menu = (
	{
		-label => 'File',
		-submenu => [
			{ -label => 'Exit	^Q', -value => \&exit_dialog }
		]
	},
);

sub exit_dialog() {
	my $return = $cui->dialog(
		-message => "Do you really want to quit?",
		-title => "Are you sure?",
		-buttons => ['yes', 'no'],
	);
	exit(0) if $return
};

my $menu = $cui->add(
	'menu', 'Menubar', -menu => \@menu, -fg => 'green',
);

my $win1 = $cui->add(
	'win1', 'Window', -border => 1, -y => 1, -bfg => 'red',
);

$cui->set_binding(sub {$menu->focus()}, "\cX");
$cui->set_binding( \&exit_dialog , "\cQ");

my $textentry = $win1->add(
	'mytextentry', 'TextEntry'
);

$textentry->focus();
my $text = $textentry->get();

$cui->error("It's the end of the\nworld as we know it!");

$cui->mainloop();
