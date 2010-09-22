goog.provide('Coworking.Application');

Coworking.Application = function() {
  if (document.getElementById('footnotes_debug')) {
    Coworking.Application._initFootnotes();
  }

  var doStats = doStats || false;
  if (doStats) {
    Coworking.Application._addStats();
  }
};

Coworking.Application._initFootnotes = function() {
  $('#footnotes_debug').hide();
  var toggle = document.createElement('input');
  $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
    $('#footnotes_debug').toggle();
  }).appendTo($(document.body));
};

Coworking.Application._addStats = function() {
  Application._addScript("http://www.google-analytics.com/ga.js");
  Application._addScript("http://www.statcounter.com/counter/counter_xhtml.js");
};

Coworking.Application._addScript = function(script_uri) {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.src = script_uri;
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(script, s);
};

$(document).ready(function() {
  new Coworking.Application();
});
