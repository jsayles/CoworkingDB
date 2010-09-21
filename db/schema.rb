# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended to check this file into your version control system.

ActiveRecord::Schema.define(:version => 20100921003253) do

  create_table "places", :force => true do |t|
    t.string    "name"
    t.integer   "parent_id"
    t.timestamp "created_at"
    t.timestamp "updated_at"
  end

  create_table "spaces", :force => true do |t|
    t.integer   "place_id"
    t.string    "name",         :null => false
    t.float     "lat"
    t.float     "long"
    t.string    "url"
    t.string    "twitter_url"
    t.string    "facebook_url"
    t.text      "description"
    t.timestamp "created_at"
    t.timestamp "updated_at"
    t.string    "address"
  end

end
