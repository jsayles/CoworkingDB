class PlacesController < ApplicationController

  def index
    @places = Place.root
  end

  def show
    @place = Place.find(params[:id])
  end

  def edit
    @place = Place.find(params[:id])
  end
  
  def update
    @place = Place.find(params[:id])
    @place.update_attributes(params[:place]) ? redirect_to(@place) : render(:action => :edit)
  end

end
