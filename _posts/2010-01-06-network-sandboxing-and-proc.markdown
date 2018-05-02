---
layout: post
title: Network sandboxing and /proc
categories: [en, blog]
tags: [exherbo, sydbox, /proc]
uuid: 5b8bd99d-a902-4d15-9d47-4ab41720bb10
---

As many of you know [sydbox](http://projects.0x90.dk/projects/show/sydbox) can
do [network sandboxing](/2009/08/27/proper-network-sandboxing) but for some
reasons we didn't have it on by default on
[Exherbo](http://www.exherbo.org).

For those who don't know much about
[sydbox](http://projects.0x90.dk/projects/show/sydbox) and network sandboxing
let me explain it briefly. Network sandboxing has three modes:

* **allow**: All network connections are allowed.
* **local**: Only local network connections are allowed.
* **deny**: No network connections are allowed.

In addition to that there's a **restrict\_connect** option which disallows
connects to all addresses except addresses that one of the parents has
[bind()](http://linux.die.net/man/2/bind)'ed to.

There's also a network white list which specifies the additional
network addresses that are allowed in **local** and **deny** modes.

On [Exherbo](http://www.exherbo.org) we use the mode **local** with
**restrict\_connect** option enabled.

One limitation of sydbox was it couldn't white list
[bind()](http://linux.die.net/man/2/bind) addresses whose port were zero.
The reason is obvious. The only place we can look up the actual port is
<tt>/proc/net/tcp</tt>, or <tt>/proc/net/tcp6</tt> for
[ipv6](http://en.wikipedia.org/wiki/Ipv6), and we need to do this before the
[bind()](http://linux.die.net/man/2/bind) call has completed. The problem arises
here. The <tt>/proc/net/tcp</tt> entry is only created after the
[bind()](http://linux.die.net/man/2/bind) call has succeeded.

The solution isn't entirely trivial. We have to note the file descriptor
argument of [bind()](http://linux.die.net/man/2/bind) along with the socket
family and socket address and intercept the subsequent
[listen()](http://linux.die.net/man/2/listen) call. Only then we can look up
the port argument from <tt>/proc/net/tcp</tt>.

The [sydbox](http://projects.0x90.dk/projects/show/sydbox)
[master](http://projects.0x90.dk/repositories/show/sydbox) has a simple
implementation to solve this problem. If the port argument of a
[bind()](http://linux.die.net/man/2/bind) call is zero, we save the file
descriptor and the corresponding socket family and address to a
[GHashTable](http://library.gnome.org/devel/glib/stable/glib-Hash-Tables.html).
After that the subsequent [listen()](http://linux.die.net/man/2/listen) call is
intercepted and if the file descriptor of the
[listen()](http://linux.die.net/man/2/listen) call matches a file descriptor in
the hash table, [sydbox](http://projects.0x90.dk/projects/show/sydbox) looks up the
port from <tt>/proc/net/tcp</tt>, fills it in and white lists the address.

With sydbox-0.4, which I'll release after some testing, network sandboxing will
be on by default again for the [Paludis](http://paludis.pioto.org) profile.

Just to be on the secure side ;)
