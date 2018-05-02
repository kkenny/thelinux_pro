---
layout: post
title: Bringing Last.fm home with mpdcron
categories: [en, blog]
tags: [mpdcron, last.fm, sqlite]
uuid: 5641fdd7-0c7e-465c-b940-69af8e41566a
---

I've been working on an [mpdcron](/mpdcron) module to save
[mpd](http://mpd.wikia.com) song data, like play count, to a local
[sqlite](http://www.sqlite.org) database. Build mpdcron like:

    $> ./configure --enable-gmodule --with-standard-modules=all
    $> make
    $> sudo make install

Then add:

    [main]
    modules = stats

to your configuration file.

Of course just saving the data isn't enough. We need a client to manipulate the
data and interact with [mpd](http://mpd.wikia.com) using this data.

Thus <tt>eugene</tt> was born.

### Usage:
First create your database:

    $> eugene update
    Updating /
    Successfully processed 12283 songs

Note this phase is optional. All other <tt>eugene</tt> commands will create the
database if it doesn't exist.

Basic interaction with the database:

    # Love/Hate/Kill/Unkill the current playing song
    $> eugene love/hate/kill/unkill
    # Love/Hate/Kill/Unkill the current playing artist
    $> eugene love/hate/kill/unkill --artist
    # Love/Hate/Kill/Unkill the current playing album
    $> eugene love/hate/kill/unkill --album
    # Love/Hate/Kill/Unkill the current playing genre
    $> eugene love/hate/kill/unkill --genre
    # Give the current playing song a rating of 10
    $> eugene rate 10
    # Increase the rating of the current playing song by 5
    $> eugene rate --add 5
    # Decrease the rating of the current playing song by 10
    $> eugene rate --substract 10

Advanced interaction with the database using the **--expr** switch:

    # Love all songs whose artist includes the string Beatles
    $> eugene love --expr 'artist like "%Beatles%"'
    # Hate all songs whose genre is Pop
    $> eugene hate --expr 'genre="Pop"'
    # Kill all songs whose duration is less than 10 seconds
    $> eugene kill --expr 'duration < 10'
    # Unkill all songs whose play count is more than 10
    $> eugene unkill --expr 'play_count > 10'

For more information about the expression syntax see:  
[http://www.sqlite.org/lang_expr.html](http://www.sqlite.org/lang_expr.html)  
To learn more about the database layout see:  
[src/gmodule/stats/stats-sqlite.c](http://github.com/alip/mpdcron/blob/master/src/gmodule/stats/stats-sqlite.c)

Loading songs to [mpd](http://mpd.wikia.com) queue:

    # Load all loved songs, exclude killed ones
    $> eugene load --expr 'love > 0 and kill != 0'
    # Clear the playlist and load all songs with a duration less than 30 seconds
    $> eugene load --clear --expr 'duration < 30'

This is all very basic right now and possibly buggy.  
If you're interested please check it out and tell me about it!
I plan to release <tt>mpdcron</tt>-0.3 after some testing.

Last but not least:  
Careful with that axe, Eugene!  
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!
