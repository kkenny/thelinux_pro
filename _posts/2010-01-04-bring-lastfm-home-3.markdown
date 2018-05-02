---
layout: post
title: Bringing Last.fm home with mpdcron (part 3)
categories: [en, blog]
tags: [mpdcron, last.fm, sqlite, ruby, nokogiri, chronic]
uuid: 97d10533-1112-4fc2-b0e2-b1a85d135338
---

I wrote a script to import [Last.fm](http://last.fm) data to
[mpdcron](/mpdcron)'s statistics database with the name <tt>homescrape</tt>.

It's written in [ruby](http://www.ruby-lang.org/) and requires
[nokogiri](http://nokogiri.org/) to parse HTML. Currently it can import play
count and loved songs. By default it will import all your
[Last.fm](http://last.fm) tracks and if you don't want that you can pass a date
using the **--since** option. Optionally <tt>homescrape</tt> can make use of
[chronic](http://chronic.rubyforge.org/) to parse dates in a huge variety of
date and time formats.

With this, the statistics module is complete feature-wise and I'll release
<tt>mpdcron</tt>-0.3 after some testing.
