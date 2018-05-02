---
layout: post
title: Bringing Last.fm home with mpdcron (part 2)
categories: [en, blog]
tags: [mpdcron, last.fm, sqlite]
uuid: 70fe949f-00cf-475c-8e77-8860b7ce5c37
---

First of all, happy new year to everyone!

After my first [post](/2009/12/26/bringing-lastfm-home) I've done many things to
improve this statistics module of [mpdcron](/mpdcron). Here's a list of major
improvements:

### Client/Server protocol
After discussing on [IRC](irc://irc.freenode.net/mpd) with
[qball](http://blog.sarine.nl/), we've decided that it's a better idea to build
a network abstraction so that clients won't access the
[sqlite](http://www.sqlite.org/) database directly.
The [protocol](/mpdcron/modules/protocol.html) will simply be like
[mpd protocol](http://www.musicpd.org/doc/protocol/) with minor differences.

I used [GIO](http://library.gnome.org/devel/gio/unstable/)
to implement the server. GIO has a
[high level network API](http://library.gnome.org/devel/gio/unstable/highlevel-socket.html)
as of version 2.22.

### Tagging
This was one of the things I really wanted to implement before releasing a new
version. Tagging songs as you would do with mail is a really nice way to sort
your music in my opinion. Tags are implemented as a colon delimited list and
uses just one **TEXT** column of a row. This makes removing a tag a slow
operation but after reading the
[sqlite optimization FAQ](http://web.utk.edu/~jplyon/sqlite/SQLite_optimization_FAQ.html)
I managed to reduce this slowness a lot making it not noticeable.

The documentation on the [website](/mpdcron) is up to date so if you want to
give it a shot you can read the [documentation](/mpdcron/modules/#stats) and start
using it right away. It's very simple.
