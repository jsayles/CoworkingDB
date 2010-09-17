// Place your application-specific JavaScript functions and classes here
// This file is automatically included by javascript_include_tag :defaults
$(document).ready(function() {
  $('#footnotes_debug').each(function() {

    $('#footnotes_debug').hide();
    var toggle = document.createElement('input');
    $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
      $('#footnotes_debug').toggle();
    }).appendTo($(document.body));
  });
});
