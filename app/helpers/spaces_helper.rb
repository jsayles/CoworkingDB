module SpacesHelper

  def name_with_place(space)
    space.place ? "#{space.name}, #{content_tag(:em, space.place.name)}".html_safe : space.name
  end

end
