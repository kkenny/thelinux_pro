---
layout: post
title: Editing SPL playlists using VIM
categories: [en, blog]
tags: [playlist, samsung, yp-u4, spl, vim]
uuid: 0c8e9205-1629-4470-9607-e8bcd2d6af06
---

I've bought a [Samsung YP-U4](http://bit.ly/yp-u4) media player recently. It can
play [Vorbis](http://www.vorbis.com/) files, in addition to <tt>mp3</tt> files.

One problem I've faced was its weird format for playlists. To edit these files
with [VIM](http://www.vim.org/) I've edited my <tt>.vimrc</tt> like this:

{%highlight vim %}

    augroup spl
    au!

    au BufRead,BufNewFile *.spl setlocal bomb ff=dos fenc=utf-16le
    augroup END " augroup spl

{%endhighlight %}

Another thing to note is <tt>\</tt> is used as the path separator. Here's how a
playlist looks like:

    SPL PLAYLIST
    VERSION 1.00

    \Music\soundtracks\crossing_the_bridge\02-tavus_havasi-live.ogg
    \Music\soundtracks\crossing_the_bridge\13-ehmedo-live.ogg
    \Music\zulfu_livaneli\cd_2\2-07_merhaba.ogg
    \Music\zulfu_livaneli\cd_2\2-12_duvarlar.ogg
    \Music\zulfu_livaneli\cd_2\2-09_o_zgu_rlu_k.ogg
    \Music\ciwan_haco\le_dine.ogg

    END PLAYLIST
