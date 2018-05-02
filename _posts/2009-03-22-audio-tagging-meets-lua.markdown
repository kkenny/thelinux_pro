---
layout: post
title: Audio Tagging Meets Lua
categories: [en, blog]
tags: [audio, envtag, lua]
uuid: 2eb5c7d4-4390-43ac-940b-2039c2a60467
---

I've just added [Lua](http://www.lua.org) scripting support to envtag.  
This makes it possible to run Lua scripts on audio tags, enabling you to play
with them through a simple Lua interface.  
Audio properties like bitrate, samplerate can also be retrieved through the same
interface.  
By interface I mean two [Lua](http://www.lua.org) tables named
__tag__ and __prop__ , which have __get()__ and __set()__ functions :)  
There are some examples under _examples/lua_ directory of the source tree if
you're interested.

This was a quick attempt to add [Lua](http://www.lua.org) support and I don't
think it's perfect yet but it works for me.  
If you want me to change it in a way that's more useful, please comment and/or
email me explaining how :)
