function footnotes_hide() {
  $('#footnotes_debug').hide();
  var toggle = document.createElement('input');
  $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
    $('#footnotes_debug').toggle();
  }).appendTo($(document.body));
}



function initMap() {
  var myLatlng = new google.maps.LatLng(47.616, -122.323);
  var myOptions = {
    zoom: 16,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), myOptions);
}

$(document).ready(function() {
  $('#footnotes_debug').each(footnotes_hide);
  $('#map').each(initMap);
});
