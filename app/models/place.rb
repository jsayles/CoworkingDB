class Place < ActiveRecord::Base

  validates_presence_of :name
  validates_uniqueness_of :name
  has_many :spaces
  acts_as_tree

  def name_with_space_count
    spaces.any? ? "#{name} (#{spaces.count})" : name
  end

  def lineage
    list = []
    if parent
      list << parent
      list << parent.lineage
    end
    list.flatten
  end

  def descendants
    list = []
    if children.any?
      children.each do |child|
        list << child
        list << child.descendants
      end
    end
    list.flatten
  end

  def all_spaces
    list = []
    list << spaces
    if descendants.any?
      descendants.each do |descendant|
        list << descendant.spaces
      end
    end
    list.flatten
  end

end
