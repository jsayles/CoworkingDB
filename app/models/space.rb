class Space < ActiveRecord::Base

  validates_presence_of :name
  validates_uniqueness_of :name
  belongs_to :place

  accepts_nested_attributes_for :place, :reject_if => lambda { |a| a[:name].blank? }



  def details?
    url? || twitter_url?
  end

end
