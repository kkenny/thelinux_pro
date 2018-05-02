---
layout: post
title: Proper network sandboxing
categories: [en, blog]
tags: [exherbo, sydbox]
uuid: ff7dda18-7b42-4e74-b8ba-3f56190712d5
---

Now that `addpredict` is
[dead]({{site.url}}/english/2009/08/22/deprecating-addpredict.html), the next thing to
implement for [sydbox]({{site.url}}/sydbox) is
proper network sandboxing. I've been working for the past three days to do that.

First of all let's define what we want:
- A way to intercept [socket()](http://linux.die.net/man/2/socket) family calls.
- The ability to deny only non-local connections.
- The ability to deny [connect()](http://linux.die.net/man/2/connect)'s to only
  addresses that were [bind()](http://linux.die.net/man/2/bind)'ed by
  children that were running under the same [sydbox](/sydbox) instance.
- Ability to [whitelist](http://en.wikipedia.org/wiki/Whitelist) certain addresses.

The first is easy. We already have a framework for intercepting many system
calls and adding support for `socket()` wasn't a problem. The only problem is on
architectures which has the
[socketcall()](http://linux.die.net/man/2/socketcall) system call and implement
all other calls on top of this single system call, we need to decode this
`socketcall()` into it's subcalls. So we need two functions
`trace_decode_socketcall` and `trace_get_addr`. Implementing those were easy
because [strace](http://sourceforge.net/projects/strace) already has similar functions.

Now that we can intercept socket calls the next step is to deny only non-local
connections. This means just checking the address of the connection if it
matches `127.0.0.1` or `::1`. Simple and efficient.

The third step is somewhat complicated. We have to check the return value of
bind calls and if they succeeded, note these addresses and corresponding ports.
This means a form of whitelist is required.

Having implemented the whitelist for step 3, it was easy to expand it to take its
elements from user configuration file or magic commands.

It's all done! Here's how it looks like in the configuration file:

    [main]
    ...
    # whether sydbox should do network sandboxing
    # defaults to false
    network = false
    ...
    # Network specific options are specified in the net group
    [net]
    # Network sandboxing default
    # One of allow, deny, local
    # Defaults to allow
    default = allow

    # Whether connect(2) requests should be restricted to addresses that were
    # bind(2)'ed by one of the parents.
    # Defaults to false
    restrict_connect = false

    # Additional addresses to be allowed when restrict_connect is set.
    # This is a list of addresses in one of the possible forms:
    # unix:///path/to/socket
    # inet://ipv4_address:port
    # inet6://ipv6_address:port
    whitelist = unix:///var/run/nscd/socket

In addition to that there are magic commands so that the package mangler can
change those options at runtime. See the manual page for more information.

**Update** : Fixed links thanks to cuerty.
