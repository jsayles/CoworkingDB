class DirectoryController < ApplicationController

  def index
    @spaces = Space.order("name ASC")
    @places = Place.where("parent_id IS NULL").order("name ASC")
  end
end
