var Application = function() {
  if (document.getElementById('footnotes_debug')) {
    Application._initFootnotes();
  }
  if (document.getElementById('map')) {
    this.map = new Application.Map('map');
  }

  var doStats = doStats || false;
  if (doStats) {
    Application._addStats();
  }
};

Application._initFootnotes = function() {
  $('#footnotes_debug').hide();
  var toggle = document.createElement('input');
  $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
    $('#footnotes_debug').toggle();
  }).appendTo($(document.body));
};

Application._addStats = function() {
  Application._addScript("http://www.google-analytics.com/ga.js");
  Application._addScript("http://www.statcounter.com/counter/counter_xhtml.js");
};

Application._addScript = function(script_uri) {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.src = script_uri;
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(script, s);
};

Application.Map = function(elementId) {
  var element = document.getElementById(elementId);
  if (element) {
    var myOptions = {
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(element, myOptions);

    var spaceData = spaceData || null;
    if (spaceData) {
      Application.Map._addSpaces(map, spaceData, true);
    }
    return map;
  }
  else{
    throw("Could not find elementId provided:" + elementId);
  }
};

Application.Map._addSpaces = function(map, spacesArray, opt_showAll) {
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
};

var application;
$(document).ready(function() {
  application = new Application();
});
