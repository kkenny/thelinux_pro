---
layout: post
title: Deprecating addpredict
categories: [en, blog]
tags: [exherbo, sydbox]
uuid: 1b2eb4b1-94ea-4cf0-aa88-6e1068cef914
---

`addpredict` is one of the commands I hate. There are many reasons for
this. First of all it's not a real fix, just a hack. If an
[exheres](http://www.exherbo.org/docs/exheres-for-smarties.html) needs
`addpredict`, it usually means the package needs fixing.

Second reason is it's really difficult to implement and it's error prone.
To implement `addpredict` using
[ptrace](http://linux.die.net/man/2/ptrace) is especially difficult for system calls
that return a [file descriptor](http://en.wikipedia.org/wiki/File_descriptor).
For predict you have to deny access to the system call but still return a valid
file descriptor. To do this we change the string argument of the system call
to `/dev/null`. This is very dangerous because we're writing to child's
memory area.

The only use case we have for `addpredict` currently in
[Exherbo](http://www.exherbo.org/) is spurious
access violations. Thinking about this and after discussing in
[#paludis](irc://irc.freenode.net/paludis) we
decided that adding access violation filters is the easiest and most secure way
to solve this problem. I added two magic commands to [sydbox](/sydbox), namely
`addfilter` and `rmfilter`. `addfilter` takes a
[fnmatch](http://linux.die.net/man/3/fnmatch)
pattern as argument and [sydbox](/sydbox) doesn't generate access violations for
paths that match this given pattern. The access to the system call is still
denied though. `rmfilter` also takes a pattern as argument and removes
it from the list of patterns. More than one pattern can be added/removed this way.

Today I added support for this to [Paludis](http://paludis.pioto.org/) and
started changing `addpredict` calls with `addfilter` in the
[Exherbo](http://www.exherbo.org) repositories. I plan to kill
`addpredict` soon.
