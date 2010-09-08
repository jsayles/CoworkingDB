class CreateSpaces < ActiveRecord::Migration
  def self.up
    create_table :spaces do |t|
      t.integer :place_id
      t.string :name
      t.string :coords
      t.string :url
      t.string :twitter
      t.text :blurb
      t.boolean :hidden
      t.timestamps
    end
  end

  def self.down
    drop_table :spaces
  end
end
