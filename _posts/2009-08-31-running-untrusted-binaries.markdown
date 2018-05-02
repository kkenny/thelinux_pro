---
layout: post
title: Running untrusted binaries that access network
categories: [en, blog]
tags: [chess, fics, icc, sydbox, timeseal, timestamp, trust]
uuid: 3caa6129-9907-4e68-8858-42f1f8e2a778
---

To compensate for network latency during playing chess games over internet,
internet chess servers like [Fics](http://www.freechess.org) and
[Icc](http://www.chessclub.com) use proprietary protocols called
[timeseal](http://www.freechess.org/Help/HelpFiles/timeseal.html) and
[timestamp](http://www.chessclub.com/help/timestamp). They distribute statically
linked stripped binaries which acts like a bridge between chess clients and the
chess server.

To make sure these tools don't do anything nasty, I use
[sydbox]({{site.url}}/sydbox) to sandbox them.
[Sydbox]({{site.url}}/sydbox)'
[master](http://github.com/alip/sydbox/tree/master) extends network
[whitelisting](http://en.wikipedia.org/wiki/Whitelist) support for network mode
deny. So I use it like:

{% highlight bash %}

    alip@harikalardiyari> cat ~/bin/timeseal
    #!/bin/sh

    SYDBOX_NO_CONFIG=1 \
    SYDBOX_NET_WHITELIST=inet://69.36.243.188:23 \
    sydbox -N -M deny -- \
    "$HOME"/bin/ics/timeseal.Linux-i386 69.36.243.188 23
    alip@harikalardiyari>

{% endhighlight %}

**SYDBOX\_NO\_CONFIG** makes [sydbox]({{site.url}}/sydbox) not read its
configuration file and **SYDBOX\_NET\_WHITELIST** adds the address, in this case
[freechess.org](http://www.freechess.org), to the network whitelist.

**edit**: Highlight code.
