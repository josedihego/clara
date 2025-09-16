# _plugins/generate_gallery.rb
Jekyll::Hooks.register :site, :pre_render do |site|
  albums = site.data['gallery']['albums']

  albums.each do |album|
    # Album page
    site.collections['albums'].docs << Jekyll::Document.new(
      site.in_source_dir("_albums/#{album['name']}.md"),
      { :site => site, :collection => site.collections['albums'] }
    ).tap do |doc|
      doc.data['layout'] = 'album'
      doc.data['title'] = album['name']
      doc.data['permalink'] = "/albums/#{album['name'].downcase}/"
    end

    # Subalbums
    album['subalbums'].each do |sub|
      site.collections['subalbums'].docs << Jekyll::Document.new(
        site.in_source_dir("_subalbums/#{album['name']}-#{sub['name']}.md"),
        { :site => site, :collection => site.collections['subalbums'] }
      ).tap do |doc|
        doc.data['layout'] = 'subalbum'
        doc.data['album'] = album['name']
        doc.data['subalbum'] = sub['name']
        doc.data['permalink'] = "/albums/#{album['name'].downcase}/#{sub['name'].downcase}/"
      end
    end
  end
end
