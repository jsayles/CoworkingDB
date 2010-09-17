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

  if (spaceData) {
    addSpaces(map, spaceData);
  }
}



function addSpaces(map, spacesArray) {
  for (var i in spacesArray) {
    var space = spacesArray[i]['space'];
    var myLatlng = new google.maps.LatLng(space['lat'], space['long']);

    var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: space['name']
    });
  }
}



function placeMarker(map, location) {
  var clickedLocation = new google.maps.LatLng(location);
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
}

$(document).ready(function() {
  $('#footnotes_debug').each(footnotes_hide);
  $('#map').each(initMap);
});
