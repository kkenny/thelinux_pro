---
layout: post
title: Recent Linux changes to help sandboxing
categories: [en, blog]
tags: [linux, sydbox, ptrace, seccomp]
lang: en
uuid: bf0d8067-7055-44d2-bfb6-15154fa83382
---

[Linux kernel 3.8][1] has been released this week which reminded me to write
about recent Linux kernel changes which may help in improving sydbox. Below is a
short summary of new, and not so new, features merely to get myself to stop
slacking and start coding again.

#### Per-process namespace support

Per-process namespace support is completed with linux-3.8. This feature provides
a nice way to separate resources on a per-process basis, for example a process
might see a set mountpoints, PID numbers, and network stack state, and a process
in other namespace might see others. For more information see the
[Linux-3.8 Changes][2] page on [kernelnewbies][3] and
the [Namespaces in Operation][4] articles on [LWN][5].

#### PTRACE\_O\_EXITKILL

New in linux-3.8, this `ptrace(2)` option makes the tracer send `SIGKILL` to
tracees on exit. This is useful for `ptrace(2)` based sandboxes for which a
resumed tracee is a security risk. See [the related commit][6] for more
information.

#### SECCOMP\_MODE\_FILTER

This is by far my favourite feature. Introduced with [Linux kernel 3.5][7] and
also known as [seccomp mode 2][8] or user filters this feature lets you add
basic system call filters expressed as [Berkeley Packet Filter][9] programs.
Even though sydbox still has to use `ptrace(2)` to do more sophisticated
argument checking, this feature removes the need to stop the tracee on every
system call entry and exit which is a PITA especially when tracing multithreaded
programs. [sydbox-1][10] takes advantage of this feature using
`SECCOMP_RET_TRACE` which signals the tracer with the new `ptrace(2)` event
`PTRACE_EVENT_SECCOMP`.

Here are some useful links:

- [Using simple seccomp filters](http://outflux.net/teach-seccomp/)
- [A library for seccomp filters](https://lwn.net/Articles/494252/)
- [vsftpd's seccomp sandbox](ftp://vsftpd.beasts.org/users/cevans/untar/vsftpd-3.0.0/seccompsandbox.c)
- [openssh's seccomp filter](http://hg.mindrot.org/openssh/rev/f40779d28db5)
- [seccomp filtering with systemd](https://plus.google.com/115547683951727699051/posts/cb3uNFMNUyK)

#### PTRACE\_SEIZE & PTRACE\_INTERRUPT

Probably even older than seccomp user filters, these ptrace requests allow the
tracer to attach to tracee without trapping it or affecting its job control
states. See,
[http://thread.gmane.org/gmane.linux.kernel/1136930](http://thread.gmane.org/gmane.linux.kernel/1136930)
for more information.

[1]: https://lkml.org/lkml/2013/2/18/476
[2]: http://kernelnewbies.org/Linux_3.8#head-789c8108e8185c402b6583480cbab3664882dfd0
[3]: http://kernelnewbies.org/
[4]: https://lwn.net/Articles/531114/
[5]: https://lwn.net/
[6]: https://git.kernel.org/linus/992fb6e170639b0849bace8e49bf31bd37c4123c
[7]: https://lkml.org/lkml/2012/7/21/114
[8]: http://kernelnewbies.org/Linux_3.5#head-c48d6a7a26b6aae95139358285eee012d6212b9e
[9]: http://en.wikipedia.org/wiki/Berkeley_Packet_Filter
[10]: http://git.exherbo.org/sydbox-1.git/
