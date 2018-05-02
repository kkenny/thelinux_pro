#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

module JekyllUtil
  # Filters posts in tags such that for every post:
  # if value is a Regex,  post[key] =~ /value/ is true
  # otherwise,            post[key] == value is true
  def self.filter_posts tags, key, value
    filtered = []
    tags.each do |tag, posts|
      filtered_posts = []
      posts.each do |post|
        case value.class
        when Regexp
          if post.data[key] =~ value then filtered_posts << post end
        else
          if post.data[key] == value then filtered_posts << post end
        end
      end
      next if filtered_posts.empty?
      filtered << [tag, filtered_posts]
    end
    filtered
  end
end
