class PlacesController < ApplicationController

  def index
    @places = Place.root
  end

  def show
    @place = Place.find(params[:id])
  end

end
