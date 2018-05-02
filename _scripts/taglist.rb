#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2010, 2011 Ali Polatel <polatel@gmail.com>

%w{fileutils rubygems jekyll byebug}.each {|m| require m}

def taglist_write(site, lang = nil)
  File.open("#{lang.nil? ? '' : "#{lang}/"}tags/index.html", 'w+') do |f|
    f.puts <<-YAML
---
layout: default
lang: #{lang.nil? ? 'all' : lang}
---
YAML

    site.tags.sort_by {|s| s[1].length }.reverse.each do |tag, posts|
      posts &= site.categories['blog']
      posts &= site.categories[lang] unless lang.nil?
      next if posts.empty?

      f.puts <<-HEADER
{% assign myvar = "#{tag}" %}
{% include handleize.liquid %}
<h1 id="{{ myid }}">#{tag.capitalize}</h2>
  <ul class="post-list">
HEADER

      posts.sort_by {|p| p.date }.reverse.each do |post|
        f.puts <<-POST
    <li>
      <h2 style="display: inline;">
        <span class="post-meta">#{post.date.strftime("%Y-%m-%d")}</span>
        <a class="post-link" href="{{ site.url }}#{post.url}">#{post.data['title']}</a>
      </h2>
    </li>
POST
      end

      f.puts <<-FOOTER
  </ul>
FOOTER
    end
  end
end

$stderr.puts "generating tag lists"

site = Jekyll::Site.new(Jekyll.configuration({
  'source' => '.',
  'destination' => '_site',
  'config' => '_config.yml'
}))
site.process

FileUtils.mkdir_p 'tags'
taglist_write(site, nil)

FileUtils.mkdir_p 'en/tags'
taglist_write(site, 'en')

FileUtils.mkdir_p 'tr/tags'
taglist_write(site, 'tr')
