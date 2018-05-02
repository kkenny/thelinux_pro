#!/usr/bin/env ruby
# coding: utf-8
# vim: set sw=2 sts=2 et nowrap fenc=utf-8 :
# Copyright 2010, 2011 Ali Polatel <polatel@gmail.com>
# Requires perl-HTML-TagCloud

%w{rubygems jekyll}.each {|m| require m}

include Jekyll::Filters

$options = Jekyll.configuration({})
$options['lsi'] = false

$site = Jekyll::Site.new($options)
$site.read_posts('')

def write_tagcloud path, lang
  # Filter tags based on language
  filtered_tags = []
  $site.tags.each do |tag, posts|
    filtered_posts = []
    posts.each { |post| if post.data['lang'] == lang then filtered_posts << post end }
    next if filtered_posts.empty?

    filtered_tags << [tag, filtered_posts]
  end

  return if filtered_tags.empty?

  commands = [
    "use warnings;",
    "use strict;",
    "use HTML::TagCloud;",
    "my $cloud = HTML::TagCloud->new(levels => #{$options['cloud_levels'].to_i});"
  ]

  filtered_tags.each do |tag, posts|
    commands << "$cloud->add(\"#{tag}\", \"#{$options['url']}tags/{% case page.lang %}{% when \\\"tr\\\" %}index-tr.html{% endcase %}##{cgi_escape(tag)}\", #{posts.length});"
  end
  commands << "print $cloud->html(#{$options['cloud_limit'].to_i});"

  perl = 'perl'
  commands.each { |c| perl << " -e '#{c}' " }
  File.open(path, 'w') { |f| f.puts `#{perl}` }
end

write_tagcloud File.join($options['cloud_directory'], 'cloud.html'), nil
write_tagcloud File.join($options['cloud_directory'], 'cloud-tr.html'), 'tr'
