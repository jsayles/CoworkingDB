#TODO should *really* only change a file if it's in source control and has no other changes

def clean_whitespace(file_name)
  lines = []
  File.open(file_name) do |file|
    file.each_line do |line|
      lines << line
    end
  end

  clean = true
  lines.each_index do |index|
    line = lines[index]
    new_line = line.gsub(/[ \t]+$/, "") #match one or more spaces/tabs at the end of the line -> nothing
    new_line = new_line.gsub(/\t/, "  ") #match all tabs and replace with two spaces

    if(new_line != line)

      if(clean)
        puts "Cleaning '#{file_name}'"
        clean = false
      end

      puts "Line #{index+1}"

      lines[index] = new_line
    end
  end

  if(!clean)
    File.open(file_name, 'w') do |file|
      lines.each { |line| file.write(line) }
    end
  end
end
