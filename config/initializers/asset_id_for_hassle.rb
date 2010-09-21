module ActionView
  module Helpers
    alias old_rails_asset_id rails_asset_id

    def rails_asset_id(source)
      asset_id = old_rails_asset_id(source)

      if(asset_id.blank?)
        path = File.join(Dir.pwd, 'tmp','hassle', source)
        asset_id = File.exist?(path) ? File.mtime(path).to_i.to_s : ''

        if @@cache_asset_timestamps
          @@asset_timestamps_cache_guard.synchronize do
            @@asset_timestamps_cache[source] = asset_id
          end
        end
      end

      asset_id
    end
  end
end