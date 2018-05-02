---
layout: post
title: Updates from pinktrace.git
categories: [en, blog]
tags: [arm, haskell, pinktrace, sydbox]
uuid: ff481c69-0a9e-457b-8f91-ec52c9b0e4f2
---

Here are some new stuff that has been cooking in
[pinktrace.git](git://github.com/alip/pinktrace.git):  

#### ARM port
I've ported [PinkTrace](http://dev.exherbo.org/~alip/pinktrace) to
[ARM](http://en.wikipedia.org/wiki/ARM_architecture). Thanks to dagger and
arachnist who have given me access to their ARM boxes. If you want to know the
technical details of this port, have a look at the file
[pink-linux-trace-arm.c](http://github.com/alip/pinktrace/blob/master/src/pink-linux-trace-arm.c).

#### Haskell bindings
I've started writing [Haskell](http://www.haskell.org/) bindings. This is a work
in progress which you can find in the
[haskell](http://github.com/alip/pinktrace/tree/haskell) branch.

#### Sydbox & PinkTrace
[Sydbox](http://git.exherbo.org/?p=sydbox.git;a=summary) requires
<tt>PinkTrace</tt> in the
[next](http://git.exherbo.org/?p=sydbox.git;a=shortlog;h=refs/heads/next)
branch. I'll merge <tt>next</tt> to <tt>master</tt> after I'm done with testing,
for which you may be of
[help](http://lists.exherbo.org/pipermail/exherbo-dev/2010-September/000718.html).

#### TODO
I've also written a
[TODO](http://github.com/alip/pinktrace/blob/master/TODO.mkd) file and added a
link to it from [Exherbo](http://www.exherbo.org)'s
[project-ideas](http://www.exherbo.org/docs/project-ideas.html) page.

This is all for now!

I've started a new university in a different city by the way and don't have a
stable internet connection these days. So if you're trying to contact me via IRC
and I'm not responding, try [email](mailto:alip@exherbo.org).
