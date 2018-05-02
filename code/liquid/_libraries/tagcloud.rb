#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

$:.unshift File.dirname(__FILE__)
require 'slugalizer'

module TagCloud
  class Perl
    attr_reader :levels, :limit, :tags

    def initialize tags, opts={}
      @levels = opts[:levels] || 24
      @limit  = opts[:limit]  || 100
      @tags   = tags
    end

    def to_html url
      perl = IO.popen('perl -w', 'w+')

      perl.puts "unshift @INC, '#{File.dirname(__FILE__)}';"
      perl.puts "use HTML::TagCloud;"
      perl.puts "my $cloud = HTML::TagCloud->new(levels => #{@levels.to_i});"
      @tags.each do |tag, posts|
        perl.puts "$cloud->add(\"#{tag}\", \"#{url}#tag-#{Slugalizer::slugalize(tag)}\", #{posts.length});"
      end
      perl.puts "print $cloud->html(#{@limit.to_i});"

      perl.close_write
      perl.read
    end
  end
end
