#/usr/bin/env ruby
# coding: utf-8
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

$:.unshift ENV['JEKYLL_LIBDIR']
%w{slugalizer tagcloud}.each {|m| require m}

module Jekyll
  class CloudTag < Liquid::Tag
    def render context
      return $cloud_cache if defined?($cloud_cache)

      site = context.registers[:site]
      cloud = TagCloud::Perl.new(site.tags,
                                 :levels => site.config['p']['cloud']['levels'],
                                 :limit  => site.config['p']['cloud']['limit'])
      url = [site.config['url'], 'tags', ""].join("/")
      cloud.to_html url
    end
  end
end

Liquid::Template.register_tag('tagcloud', Jekyll::CloudTag)
