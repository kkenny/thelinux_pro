---
layout: post
title: Lua bindings for libmpdclient-2
categories: [en, blog]
tags: [lua, libmpdclient, mpd]
uuid: 75874788-443c-424a-8f66-fcc3ceb16aed
---

I started writing [Lua](http://www.lua.org/) bindings for
[libmpdclient-2](http://mpd.wikia.com/wiki/ClientLib:libmpdclienthttp://mpd.wikia.com/wiki/ClientLib:libmpdclient).
It's a thin wrapper around libmpdclient. Here is a simple example demonstrating
usage:

{% highlight lua %}

    require "mpdclient"

    conn, errmsg = mpdclient.new("localhost", 6600, 10)
    if not conn then
        error(errmsg)
    elseif conn:get_error() ~= mpdclient.MPD_ERROR_SUCCESS then
        error(conn:get_error_message())
    end

    conn:send_status()
    status = conn:get_status()
    conn:response_finish()
    print "Mpd Status"
    print "----------"
    print("Volume: " .. status.volume .. "%")
    print("Repeat: " .. status['repeat']) -- repeat is a reserved word in Lua ;)
    print("Random: " .. status.random)
    print("Single: " .. status.single)
    print("Consume: " .. status.consume)
    print("Playlist Length: " .. status.playlist_length)
    print("Crossfade: " .. status.crossfade)
    print("Song: " .. status.song)
    print("Song ID: " .. status.songid)
    print("Time: " .. status.elapsed_time .. "/" .. status.total_time)

    if status.state == mpdclient.MPD_STATE_PLAY or
        status.state == mpdclient.MPD_STATE_PAUSE then
        conn:send_currentsong()
        entity = conn:get_next_entity()
        if not entity then
            error "Failed to find any entity!"
        elseif entity.type ~= mpdclient.MPD_ENTITY_TYPE_SONG then
            error "Entity doesn't have to expected type!"
        end
        song = entity.song
        artist = song:get_tag(mpdclient.MPD_TAG_ARTIST, 0)
        title = song:get_tag(mpdclient.MPD_TAG_TITLE, 0)
        print(artist .. " - " .. title)
    end
    conn:close() -- You can also let gc handle this
    conn = nil -- Because using the connection object after closing it will kill your kittens!

{% endhighlight %}

There is no documentation yet and there are some more functions to wrap, see
[TODO](http://github.com/alip/luampdclient/blob/master/TODO.mkd). Nevertheless
it should be usable at this stage.

**edit**: Highlight code.
