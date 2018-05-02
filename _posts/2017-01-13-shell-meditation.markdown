---
layout: post
title: Shell Meditation
categories: [en, blog]
tags: [audio, mpd, mpdcron, bach]
uuid: e58fce33-9898-4180-b083-704b499ec321
---

Seek your music. As you please.

{% highlight bash %}
    while true; do
        (( z = ${RANDOM} % 100 ))
        (( a = $z % 10 ))
        mpc seek $z% &
        sleep $a
        kill $!
        wait
    done
{% endhighlight %}
