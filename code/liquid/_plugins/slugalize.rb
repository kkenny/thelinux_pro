#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

$:.unshift ENV['JEKYLL_LIBDIR']
require 'slugalizer'

module Jekyll
  module Filters
    def slugalize input, separator='_'
      Slugalizer::slugalize(input, separator)
    end
  end
end
