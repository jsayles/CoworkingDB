class PlacesController < ApplicationController

  def index
    @places = Place.where("parent_id IS NULL OR parent_id = ''").order("name ASC")
  end
  
  def show
    @place = Place.find(params[:id])
  end

end
