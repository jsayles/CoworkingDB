var application = function() {
  if (document.getElementById('footnotes_debug')) {
    application._initFootnotes();
  }
  if (document.getElementById('map')) {
    new application.map();
  }

  var doStats = doStats || false;
  if (doStats) {
    application._addStats();
  }
};

application._initFootnotes = function() {
  $('#footnotes_debug').hide();
  var toggle = document.createElement('input');
  $(toggle).attr('id', 'footnotes_debug_toggler').attr('type', 'button').attr('value', 'FN').click(function() {
    $('#footnotes_debug').toggle();
  }).appendTo($(document.body));
};

application._addStats = function() {
  application._addScript("http://www.google-analytics.com/ga.js");
  application._addScript("http://www.statcounter.com/counter/counter_xhtml.js");
};

application._addScript = function(script_uri) {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.src = script_uri;
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(script, s);
};

application.map = function() {
  var myOptions = {
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), myOptions);

  if (spaceData) {
    application.map._addSpaces(map, spaceData, true);
  }
};

application.map._addSpaces = function(map, spacesArray, opt_showAll) {
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

$(document).ready(application);
