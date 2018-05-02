#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

$:.unshift ENV['JEKYLL_LIBDIR']
require 'slugalizer'

module Jekyll
  class TagList < Page
    def initialize(site, base, dir, name)
      @site = site
      @base = base
      @dir  = dir
      @name = name

      self.process(@name)

      # No YAML front matter
      # self.read_yaml(File.join(base, dir), name)
      self.data ||= {}
      self.data['layout'] = 'default'
      self.content = taglist
    end

    private
    def taglist
      content = []

      sorted_tags = @site.tags.sort {|a, b| b[1].length <=> a[1].length }
      sorted_tags.each do |tag, posts|
        sorted_posts = posts.sort {|a, b| b.date <=> a.date }

        # content << "<h3 id=\"tag-#{Slugalizer::slugalize(tag)}\">#{tag}</h3>"
        content << "<h3 id=\"tag-#{tag}\">#{tag}</h3>"
        content << '<ul>'
        sorted_posts.each do |post|
          content << "<li>#{post.date.strftime('%Y-%m-%d')} &raquo; <a href='#{post.url}'>#{post.data['title']}</a></li>"
        end
        content << "</ul>"
      end

      content.join "\n"
    end
  end

  class TagListGenerator < Generator
    def generate(site)
      list = TagList.new site, site.source, "tags", "index.html"
      list.render(site.layouts, site.site_payload)
      list.write(site.dest)
      site.pages << list
    end
  end
end
