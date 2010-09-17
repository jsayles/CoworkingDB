require "#{File.dirname(__FILE__)}/whitespace"

desc "Do pre-commit tasks"
task :pre => ['pre:pngcrush', 'pre:update_css', 'pre:whitespace']

namespace :pre do

  desc "Clean-up whitespace"
  task :whitespace do
    puts "Clean-up whitespace"
    source_files_pattern = File.join(RAILS_ROOT, "**", "{*.{rake,js,as,mxml,rb,sass,haml,gv,yml},Rakefile}")
    source_files = Dir.glob(source_files_pattern).select { |file| !(file =~ /vendor\/.*/) }.select { |file| !(file =~ /db\/schema.rb/) }

    source_files.each do |file|
      clean_whitespace(file)
    end

  end

  desc "Render sass -> css for production"
  task :update_css => :environment do
    puts "Render sass -> css for production"
    require 'sass_functions'
    Sass::Plugin.options[:always_update] = true
    Sass::Plugin.options[:style] = :compact
    Sass::Plugin.options[:line_comments] = false
    Sass::Plugin.update_stylesheets
  end

  desc "Crush all pngs in public/images directory"
  task :pngcrush do
    puts "Crush all pngs in public/images directory"
    app = 'pngcrush'
    if(`which #{app}`.length == 0)
      puts "Skipping crush - '#{app} does not exist. Skipping"
    else
      puts "Crushing pngs"

      img_dir = File.join(RAILS_ROOT, "public/images")
      tmp_file = File.join(RAILS_ROOT, 'tmp', 'png_to_crush.png')

      pngs = File.join(img_dir, "*.png")
      pngs = Dir.glob(pngs)
      count = 0
      pngs.each do |png|
        `pngcrush #{png} #{tmp_file}`
        if(!FileUtils.compare_file(png, tmp_file))
          count += 1
          puts "#{png} has been updated"
          `mv #{tmp_file} #{png}`
        end
      end

      if(count == 0)
        puts "nothing to crush"
      end

      FileUtils.rm(tmp_file) if File.exist?(tmp_file)
    end
  end

end
