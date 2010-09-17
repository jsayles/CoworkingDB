function footnotes_hide() {
  $('#footnotes_debug').hide();
  var toggle = document.createElement('input');
  $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
    $('#footnotes_debug').toggle();
  }).appendTo($(document.body));
}



function initMap() {
  var myOptions = {
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), myOptions);

  if (spaceData) {
    addSpaces(map, spaceData, true);
  }
}



function addSpaces(map, spacesArray, opt_showAll) {
  if (spacesArray && spacesArray.length) {
    var bounds = new google.maps.LatLngBounds();

    for (var i in spacesArray) {
      var space = spacesArray[i]['space'];
      var latLng = new google.maps.LatLng(space['lat'], space['long']);
      bounds.extend(latLng);

      var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        title: space['name']
      });
    }

    if (opt_showAll) {
      if (spacesArray.length > 1) {
        map.fitBounds(bounds);
      } else {
        map.setCenter(bounds.getCenter());
      }
    }

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
