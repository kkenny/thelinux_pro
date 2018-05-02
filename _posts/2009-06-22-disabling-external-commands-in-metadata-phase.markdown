---
layout: post
title: Disabling External Commands in Metadata Phase
categories: [en, blog]
tags: [exherbo, paludis, sydbox, exheres, metadata]
uuid: 008198c0-81c1-4453-b103-091b54fbcd13
---

Running external commands in the metadata phase of exheres/ebuild is obviously a  
bad idea because this phase is used to generate caches.

[Ciaranm](http://ciaranm.wordpress.com/) has come up with an idea to generate
[Sydbox]({{site.url}}/sydbox) access violations when  
execve() family functions are called in the metadata phase. This was rather easy  
to [implement](http://github.com/alip/sydbox/commit/6e822623d9670688a1ec88804b81896d5ab22314).

I've added two Sydbox magic commands, namely **/dev/sydbox/ban\_exec** and  
**/dev/sydbox/unban\_exec** . Writing to the former file sets the flag to ban all  
_execve()_ calls and writing to the latter unsets the flag.

A small example looks like:

    #!/bin/sh
    /bin/true # This call succeeds.
    :>/dev/sydbox/ban_exec
    /bin/true # This call fails with EACCES.
    :>/dev/sydbox/unban_exec
    /bin/true # This call succeeds.

The last thing to do was to add support to [Paludis](http://paludis.pioto.org).  
I've amended my sydbox support commit and added support to ban execve() calls in the metadata phase.  
If you're using my paludis-sydbox branch, make sure to use sydbox-scm and not  
0.1\_beta4. I think I’ll release 0.1\_beta5 with only this change but I have  
school tomorrow and I won't have internet access for two days.
