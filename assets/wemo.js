// Spin.js dynamically creates spinning activity indicators that can be used as resolution-independent replacement for AJAX loading GIFs.
// Source: http://fgnass.github.io/spin.js/
var opts = {
  lines: 13 // The number of lines to draw
, length: 28 // The length of each line
, width: 14 // The line thickness
, radius: 42 // The radius of the inner circle
, scale: 0.5 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: '#0094e0' // #rgb or #rrggbb or array of colors
, opacity: 0 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 60 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '707px' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
}
var spinner = new Spinner(opts); // Get spinner ready for presentation

// Add onclick listener to id of push button element
// Results in a jQuery based AJAX request to the same CGI containing
// POST params which will invoke a call to the activate_relay function
// which resides in the CGI.
$( document ).ready(function() {
	$('#toggle--push--glow').click(function() {
		$.ajax({
			type: 'POST',
			data: 'cmd=toggle',
			success: function(){ toggle_success() },
			error: function(){ toggle_error() },
			url: '/',
			cache:false
		});
	});
});

function toggle_success() {
	// add visual indicator of work
	spinner.spin();
	$('#spinner-container').append( spinner.el );
	// stop repeated presses of the button for duration of relay toggle
	$('#toggle--push--glow').prop( "disabled", true );
	// 2.5seconds - less results in race conditions due to delay on the WeMo relay momentary switch
	setTimeout(reset_toggle_state, 2500); 
}

function toggle_error() {
}

function reset_toggle_state() {
	// back to intial state
	$('#toggle--push--glow').prop( "checked", false );
	$('#toggle--push--glow').prop( "disabled", false );
	spinner.stop();
}
