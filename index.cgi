#!/usr/bin/perl

use strict;
use warnings;

use CGI qw( :standard );
use Try::Tiny;
use Data::Dumper;

use WebService::Belkin::WeMo::Device;
use WebService::Belkin::WeMo::Discover;

my $debug = 1;
my $wemo_lockout = 0; # useful for testing purposes to stop relay activating
my $wemo_ip = '192.168.3.220';
my $page_title = 'WeMo WebApp';
my $fail_url = 'https://google.com/fail';

my $wemo_db = 'wemo.db';
_check_wemo_db();

my $cgi = CGI->new();

my $wemo = undef;
eval { 
	$wemo = WebService::Belkin::WeMo::Device->new(
		ip => $wemo_ip,
		db => $wemo_db
	);
};
print STDERR $@ if$@;

my $params = $cgi->Vars;
if( keys %{ $params } )
{
	_process_cmd();
}

print $cgi->header();
print $cgi->start_html( 
        -title => $page_title,
	-head => [ 
		Link({ # Android Chrome >= M39 homescreen support
			-rel => 'manifest',
			-href => 'manifest.json'
		}),
		Link({ # See: https://en.wikipedia.org/wiki/Favicon
			-rel => 'icon',
			-href => 'favicon.ico'
		}),
		Link({
			-rel => 'icon',
			-sizes => '192x192',
			-href => '../assets/homescreen-icon-192.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '152x152',
			-href => '../assets/homescreen-icon-152.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '128x128',
			-href => '../assets/homescreen-icon-128.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '120x120',
			-href => '../assets/homescreen-icon-120.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '76x76',
			-href => '../assets/homescreen-icon-76.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '64x64',
			-href => '../assets/homescreen-icon-64.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '60x60',
			-href => '../assets/homescreen-icon-60.png'
		}),
		Link({
			-rel => 'icon',
			-sizes => '32x32',
			-href => '../assets/homescreen-icon-32.png'
		}),
	],
	-meta => { # Android Chrome <M39 homescreen support
		'mobile-web-app-capable' => 'yes',
		'viewport' => 'user-scalable=no, height=device-height, initial-scale=0.5'
	},
        -style => {
                -src => '../assets/screen.css'
        },
	script => [
		{
			-type => 'javascript',
			-src => '../assets/jquery-2.1.4.min.js'
		}, 
		{
			-type => 'javascript',
			-src => '../assets/spin.min.js'
		},
		{
			-type => 'javascript',
			-src => '../assets/wemo.js'
		}
	]
);

_render_wemo();

print $cgi->end_html(); 


sub _process_cmd
{
	foreach my $key( sort{ lc( $a ) cmp lc( $b ) } keys %{$params} )
	{
		if( $key eq 'cmd' )
		{
			if( $params->{ $key } eq 'toggle' )
			{
				print $cgi->header();
				print $cgi->start_html();
				print "$key = $params->{ $key }";
				print $cgi->end_html();
				_activate_relay();
				exit;
			}
		}
	}
	# if we get here we have failed to process any command
	print $cgi->redirect($fail_url);
}

sub _render_wemo
{
	my $status_led = $wemo ? '../assets/wemo-led-green.jpg' : '../assets/wemo-led-red.jpg';
	my $button_disabled = $wemo ? '' : 'disabled="disabled"';
	print qq|
	<div class="main-container">
		<img class="base-image" src="../assets/wemo.jpg"/>
		<img class="status-image" src="$status_led"/>
		<div class="toggle toggle--push toggle--push--glow">
			<input type="checkbox" id="toggle--push--glow" class="toggle--checkbox" $button_disabled>
			<label class="toggle--btn" for="toggle--push--glow" data-label-on="on"  data-label-off="off"></label>
		</div>
		<div id="spinner-container"></div>
	</div>|;
}

sub _check_wemo_db
{
	# force populate db file if it is empty
	unless( -s $wemo_db ) {
		if( $debug ) { print STDERR "Searching for new wemo devices\n"; }
		my $wemo = WebService::Belkin::WeMo::Discover->new();
		my $devices = $wemo->search();
		if( $debug ) { print STDERR "Saving wemo devices to cache db: $wemo_db\n"; }
		$wemo->save( $wemo_db );
	}
}

sub _activate_relay
{
	if( $wemo ) {
		if( $wemo_lockout ) {
			print STDERR "WeMo disabled"
		} else {
			$wemo->toggleSwitch();
		}
	} else {
		print STDERR "Unable to connect to wemo\n";
	}
}
