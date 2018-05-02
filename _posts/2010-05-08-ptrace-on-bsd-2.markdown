---
layout: post
title: ptrace on BSD (part 2)
categories: [en, blog]
tags: [bsd, freebsd, ptrace]
uuid: 8e3d5cca-079d-4ec1-a440-6ec086d38caf
---

On my [first post](/2010/01/16/ptrace-on-bsd/) with the same $topic, I've
described a ptrace bug on FreeBSD. I've reported this issue on
[freebsd-hackers](http://marc.info/?l=freebsd-hackers&m=126367014218610&w=2)
mailing list and submitted a
[PR](http://www.freebsd.org/cgi/query-pr.cgi?pr=kern/142958) and FreeBSD
developers have fixed the problem.

Here's how they did it:
- [r202882](http://svnweb.freebsd.org/viewvc/base?view=revision&revision=202882)  
- [r203608](http://svnweb.freebsd.org/viewvc/base?view=revision&revision=203608)

A big thanks!
