---
layout: post
title: Tor Patch for tsocks
categories: [en, blog]
tags: [dns, gentoo, tor]
uuid: a3c9e1d8-8341-41a5-9e17-d1c9f9de0310
---

DNS leaks are a major problem for [Tor](http://www.torproject.org/).  
Tor doesn't provide a direct solution to that but there are still some ways to  
solve this problem.  
One of the solutions is _dns-proxy-tor_ which is a DNS server that constructs  
[Tor](http://www.torproject.org/) to map a domain to a virtual IP address and  
subsequently [Tor](http://www.torproject.org/) will treat the virtual IP address  
as an alias for the original domain name.

The other solution is a patch written by _Total Information Security_ which  
modifies _tsocks_ . With this patch _tsocks_ uses SOCKS for name resolution  
which both prevents DNS leaks and enables direct access to _.onion_ addresses  
for torified programmes.  
Without the patch one has to add mapaddress lines to his/her torrc to map
domains to virtual IP addresses.

Yesterday I wrote a [bug report](https://bugs.gentoo.org/show_bug.cgi?id=148550)
about this to [Gentoo Bugzilla](https://bugs.gentoo.org/) to add a __tordns__  
USE flag to tsocks and developers have added it to portage. This is what I love  
about Gentoo. You request a feature and if it's acceptable it'll be added  
before you wake up next day :)
