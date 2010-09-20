Application.Searcher = function(searchFieldId, statusId, addressFieldId, latFieldId, longFieldId, map) {
  this.m_inputField = document.getElementById(searchFieldId);
  this.m_latField = document.getElementById(latFieldId);
  this.m_longField = document.getElementById(longFieldId);
  this.m_addressField = document.getElementById(addressFieldId);
  this.m_statusDiv = document.getElementById(statusId);
  this.m_map = map;
};

Application.Searcher.prototype.update = function() {
  var searchString = this.m_inputField.value;
  this._searchAddress(searchString, this._success, this._error);
  this._status("Searching...");
};

Application.Searcher.prototype._searchAddress = function codeAddress(searchString) {
  var _this = this;
  if (!Application.Searcher._geocoder) {
    Application.Searcher._geocoder = new google.maps.Geocoder();
  }

  Application.Searcher._geocoder.geocode({
    'address': searchString
  },
  function(results, status) {
    if (status != google.maps.GeocoderStatus.OK) {
      _this._error("There was an error from the Google Geocoder:" + status);
      return;
    } else if (results.length > 1) {
      _this._error("Got more than one result. Can you be more specific?");
      return;
    }
    var result = results[0];
    if (result.geometry.location_type != "ROOFTOP") {
      _this._error("Couldn't exactly find this space. Could you be more specific?");
      return;
    } else {
      _this._success(result.geometry.location, result.formatted_address);
    }
  });
};

Application.Searcher.prototype._success = function(location, newAdress) {
  $(this.m_addressField).val(newAdress);
  $(this.m_latField).val(location.lat());
  $(this.m_longField).val(location.lng());

  if(this.m_marker){
    this.m_marker.setMap(null);
  }

  this.m_marker = new google.maps.Marker({
    position: location,
    map: this.m_map
  });

  this._status('Success!');
  this.m_map.setCenter(location);
};

Application.Searcher.prototype._error = function(message) {
  this._status(message);
};

Application.Searcher.prototype._status = function(message) {
  if (message) {
    $(this.m_statusDiv).show().text(message);
  } else {
    $(this.m_statusDiv).hide().text('');
  }
};

var searcher;
$(document).ready(function() {
  searcher = new Application.Searcher('searchField', 'searchStatus', 'address', 'lat', 'long', application.map);
  searcher.update();
});
