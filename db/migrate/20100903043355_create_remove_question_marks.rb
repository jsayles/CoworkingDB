class CreateRemoveQuestionMarks < ActiveRecord::Migration
  def self.up
    rename_column :places, :locked?, :locked
  end

  def self.down
    rename_column :places, :locked, :locked?
  end
end
