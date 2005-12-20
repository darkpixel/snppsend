#!/usr/bin/perl -w

use strict;
use Data::Dumper;
use Gtk2 '-init';

my $window = Gtk2::Window->new;
$window->set_title ('\'X\'snppsend');

$window->signal_connect (destroy => sub { Gtk2->main_quit; });

my $button = Gtk2::Button->new ('Click Me To Quit');

my $user_data = 'Hello';
$button->signal_connect (clicked => \&button_callback, $user_data);
$window->add ($button);
$window->show_all;
Gtk2->main;

sub button_callback 
{
        print Dumper (@_);
        Gtk2->main_quit;
        1;
}