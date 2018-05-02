#!/usr/bin/env ruby
# coding: utf-8
# Copyright 2010, 2011, 2012 Ali Polatel <polatel@gmail.com>

%w{rubygems jekyll}.each {|m| require m}

# Must be in sync with _includes/handleize.liquid
def handleize tag
  t = tag.gsub('ç', 'c').gsub('ğ', 'g').gsub('ı', 'i').gsub('ö', 'o').gsub('ş', 's').gsub('ü', 'u')
  t = t.gsub('+', 'plus').gsub('-', 'minus')
  t = t.gsub(' ', '_').gsub('/', ':')
  "tag-" + t.downcase
end

module TagCloud
  class Perl
    def initialize site, opts={}
      @site   = site
      @levels = opts[:levels] || 24
      @limit  = opts[:limit]  || 100
    end

    def write_html lang=nil
      perl = IO.popen("perl -w -I'#{File.expand_path(File.dirname(__FILE__))}'", 'w+')

      perl.puts <<EOF
use HTML::TagCloud;
my $cloud = HTML::TagCloud->new(levels => #{@levels.to_i});
EOF
      @site.tags.each do |tag, posts|
        posts &= @site.categories['blog']
        posts &= @site.categories[lang] unless lang.nil?
        next if posts.empty?

        perl.puts <<EOF
$cloud->add("#{tag}", '{{ site.url }}#{lang.nil? ? '/' : "/#{lang}"}/tags/##{handleize(tag)}', #{posts.length});
EOF
      end
      perl.puts "print $cloud->html(#{@limit.to_i});"

      perl.close_write
      File.open("_includes/cloud#{lang.nil? ? '' : '-'}#{lang}.html", 'w+') {|f| f.puts perl.read}
    end
  end
end

$stderr.puts "generating tag cloud"

site = Jekyll::Site.new(Jekyll.configuration({
  'source' => '.',
  'destination' => '_site',
  'config' => '_config.yml'
}))
site.process

cloud = TagCloud::Perl.new(site)
cloud.write_html nil
cloud.write_html 'en'
cloud.write_html 'tr'
