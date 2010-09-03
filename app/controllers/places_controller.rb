class PlacesController < ApplicationController

  def index
    @places = Place.order("name ASC")
  end

end
