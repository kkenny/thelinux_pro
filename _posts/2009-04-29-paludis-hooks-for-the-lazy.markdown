---
layout: post
title: Paludis Hooks For The Lazy
categories: [en, blog]
tags: [paludis, locale-gen]
uuid: d1b345a6-7962-4db3-b20c-213290d8465f
---

I've just created a
[repository](http://github.com/alip/paludis-hooks/tree/master) to publish my [Paludis](http://paludis.pioto.org)
hooks.  
Right now there are two simple hooks in the repository.  
The first
[one](http://github.com/alip/paludis-hooks/blob/master/auto/locale-gen.hook)
is to generate locales after glibc updates.  
You can think this as a locale-gen equivalent for
[Exherbo](http://www.exherbo.org).  
The second
[one](http://github.com/alip/paludis-hooks/blob/master/auto/zoneinfo.hook)
updates /etc/localtime when timezone-data is updated.
