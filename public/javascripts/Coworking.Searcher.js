Coworking.Searcher = function(searchFieldSelector, statusSelector, addressFieldSelector, latFieldSelector, longFieldSelector, map) {
  this.m_inputSelector = searchFieldSelector;
  this.m_latSelector = latFieldSelector;
  this.m_longSelector = longFieldSelector;
  this.m_addressSelector = addressFieldSelector;
  this.m_statusSelector = statusSelector;
  this.m_map = map;
};

Coworking.Searcher.prototype.update = function() {
  var searchString = $(this.m_inputSelector).val();
  this._searchAddress(searchString, this._success, this._error);
  this._status("Searching...");
};

Coworking.Searcher.prototype._searchAddress = function codeAddress(searchString) {
  if (!Coworking.Searcher._geocoder) {
    Coworking.Searcher._geocoder = new google.maps.Geocoder();
  }

  Coworking.Searcher._geocoder.geocode({
    'address': searchString
  },
  goog.bind(this._geocodeResult, this)
  );
};

Coworking.Searcher.prototype._geocodeResult = function(results, status) {
  if (status != google.maps.GeocoderStatus.OK) {
    this._error("There was an error from the Google Geocoder:" + status);
    return;
  } else if (results.length > 1) {
    this._error("Got more than one result. Can you be more specific?");
    return;
  }
  var result = results[0];
  if (result.geometry.location_type != "ROOFTOP") {
    this._error("Couldn't exactly find this space. Could you be more specific?", result.geometry.bounds);
    return;
  } else {
    this._success(result.geometry.location, result.formatted_address);
  }
};

Coworking.Searcher.prototype._success = function(location, newAdress) {
  $(this.m_addressSelector).val(newAdress);
  $(this.m_latSelector).val(location.lat());
  $(this.m_longSelector).val(location.lng());

  this._clearMarker();

  this.m_marker = new google.maps.Marker({
    position: location,
    map: this.m_map
  });

  this._status('Success!');
  if (this.m_map.getCenter()) {
    this.m_map.panTo(location);
  } else {
    this.m_map.setCenter(location);
  }
  this.m_map.setZoom(16);
};

Coworking.Searcher.prototype._error = function(message, opt_bounds) {
  this._clearMarker();
  this._status(message);
  if (opt_bounds) {
    this.m_map.fitBounds(opt_bounds);
  }
};

Coworking.Searcher.prototype._status = function(message) {
  if (message) {
    $(this.m_statusSelector).show().text(message);
  } else {
    $(this.m_statusSelector).hide().text('');
  }
};

Coworking.Searcher.prototype._clearMarker = function() {
  if (this.m_marker) {
    this.m_marker.setMap(null);
    this.m_marker = null;
  }
};
