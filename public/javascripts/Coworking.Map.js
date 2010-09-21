goog.provide('Coworking.Map');

Coworking.Map = function(elementId) {
  var element = document.getElementById(elementId);
  if (element) {
    var myOptions = {
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.m_map = new google.maps.Map(element, myOptions);
  } else {
    throw ("Could not find elementId provided:" + elementId);
  }
};

Coworking.Map.prototype.getGoogMap = function(){
  return this.m_map;
};

Coworking.Map.prototype.populateSpaces = function(spacesArray, opt_showAll) {
  if (spacesArray && spacesArray.length) {
    var bounds = new google.maps.LatLngBounds();

    for (var i in spacesArray) {
      var space = spacesArray[i]['space'];
      var latLng = new google.maps.LatLng(space['lat'], space['long']);
      bounds.extend(latLng);

      var marker = new google.maps.Marker({
        position: latLng,
        map: this.m_map,
        title: space['name']
      });
    }

    if (opt_showAll) {
      if (spacesArray.length > 1) {
        this.m_map.fitBounds(bounds);
      } else {
        this.m_map.setCenter(bounds.getCenter());
      }
    }

  }
};
