class SpacesController < ApplicationController

  def index
    @spaces = Space.order("name ASC")
  end

  def new
    @space = Space.new(params[:space])
    @space.build_place

  end

  def create
    @space = Space.new(params[:space])
    if @space.save
      redirect_to @space
    else
      render :action => :new
    end

  end

  def show
    @space = Space.find(params[:id])
  end

  def edit
    @space = Space.find(params[:id])
  end

  def update
    @space = Space.find(params[:id])
    @space.update_attributes(params[:space])
    flash[:notice] = "#{@space.name} updated."
    redirect_to @space
  end

end
