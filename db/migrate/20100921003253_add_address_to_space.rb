class AddAddressToSpace < ActiveRecord::Migration
  def self.up
    add_column :spaces, :address, :string
  end

  def self.down
    remove_column :spaces, :address
  end
end
