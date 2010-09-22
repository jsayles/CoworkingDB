class CreateSpaces < ActiveRecord::Migration
  def self.up
    create_table :spaces do |t|
      t.integer :place_id
      t.string :name, :null => false
      t.decimal :lat, :precision => 15, :scale => 10
      t.decimal :long, :precision => 15, :scale => 10
      t.string :url
      t.string :twitter_url
      t.string :facebook_url
      t.text :description
      t.timestamps
    end
  end

  def self.down
    drop_table :spaces
  end
end
