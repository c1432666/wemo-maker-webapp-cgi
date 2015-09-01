# wemo-maker-webapp-cgi
Contains a CGI based WebApp for controlling a Belkin WeMo Maker

- All relevant metadata and images are present to allow the page to be added
to homescreen of Android device as a "WebApp":
https://developer.chrome.com/multidevice/android/installtohomescreen
http://developer.android.com/guide/webapps/targeting.html

- Rendered via Perl's CGI.pm
http://perldoc.perl.org/CGI.html
http://search.cpan.org/dist/CGI/

- JQuery used for convenience around AJAX POST requests.

- CSS3 elements used for toggle-button overlay.
http://codepen.io/ashleynolan/pen/wBppKz
https://github.com/ashleynolan/toggle-buttons

- Spin.js used for timer indicator.
http://spin.js.org
http://fgnass.github.io/spin.js/

- WebService::Belkin::WeMo perl modules used for uPnP interface to WeMo hardware.
http://search.cpan.org/~ericblue/WebService-Belkin-WeMo-1.0/

INSTALLATION
============
Expects to be served by a web server, e.g. Apache.
Put the entire bundle somewhere in your document root and ensure index.cgi is executable.

PRE-REQS
========
No other dependencies except the Perl modules:
CGI
WebService::Belkin::Wemo:Device
WebService::Belkin::Wemo:Discover
