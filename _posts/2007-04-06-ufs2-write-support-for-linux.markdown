---
layout: post
title: UFS2 write support for Linux
categories: [en, blog]
tags: [freebsd, gentoo, ufs2, ext3, dualboot]
uuid: caa5cf9f-0e73-40b5-930e-317238bfbc00
---

I've been dual booting
[Gentoo/FreeBSD](http://www.gentoo.org/proj/en/gentoo-alt/bsd/fbsd/) and
[Gentoo](http://www.gentoo.org) for a while and one problem I've faced is a
decent filesystem for the operating systems to share. FreeBSD has read-write
support for ext2 and read-only support for reiserfs. ext3 is also supported
as it's backwards compatible with ext2.

Well ext3 is a cool filesystem to use but I've been experiencing weird problems
with it on FreeBSD. So I went on to check for Linux kernel changes today to see
if there's any plan to add UFS2 write support anytime in the future. I was
shocked :). There are already patches written and it's planned to be added in
2.6.21. I quickly got git-sources and tried it. It works like charm so far.
I can mount ufs2 partitions r/w on both systems. Many thanks to Evgeniy Dushistov
who wrote the patches.

The patches are here:

* [PATCH 1/3](http://lkml.org/lkml/2007/1/29/192) UFS2 write: mount as rw
* [PATCH 2/3](http://lkml.org/lkml/2007/1/29/193) UFS2 write: inodes write
* [PATCH 3/3](http://lkml.org/lkml/2007/1/29/194) UFS2 write: block allocation update
