---
layout: post
title: Pink's Tracing Library
categories: [en, blog]
tags: [catbox, exherbo, pardus, ptrace, pinktrace, sydbox]
uuid: 4ba0d9ff-7e50-480d-aeba-2132469d16b7
---

As many of you know I've written
[sydbox](http://projects.0x90.dk/projects/show/sydbox), the default sandbox of
[Exherbo](http://www.exherbo.org) [Linux](http://kernel.org) distribution. For a
long time I've been meaning to move the platform-dependent parts of
<tt>sydbox</tt> to a library, so that others can make use of it.

Last week, I've started writing a library called
[pinktrace](http://dev.exherbo.org/~alip/pinktrace) aka Pink's Tracing Library.
This library is aimed to be a cross-platform lightweight
[ptrace](http://en.wikipedia.org/wiki/Ptrace) library. It provides:

- Wrappers around different <tt>ptrace</tt> requests.
- An API for decoding arguments (strings, socket addresses, ...)
- An **experimental** API for encoding arguments.

You can read more about it [here](http://dev.exherbo.org/~alip/pinktrace).  
An extensive API reference is available
[here](http://dev.exherbo.org/~alip/pinktrace/api/c).  
[Python](http://dev.exherbo.org/~alip/pinktrace/api/python) and
[Ruby](http://dev.exherbo.org/~alip/pinktrace/api/ruby) bindings are available
as well.

So what's next? I'll write another library, which will probably be called
<tt>libsydbox</tt>, which builds on top of <tt>pinktrace</tt> and <tt>GLib</tt>.
This will be a sandboxing library which can be used to sandbox untrusted
applications. I'll also write Python bindings for it which will hopefully
replace [catbox](http://svn.pardus.org.tr/uludag/trunk/catbox/) of
[Pardus](http://www.pardus.org.tr/eng/) Linux distribution.
Here's how it will look like:

                    Sydbox (A simple
                      ^     application using libsydbox)
                      |
                      |-------> pysydbox (Python bindings for libsydbox
                      |                   which aims to replace catbox)
                      |
                  libsydbox (Implements
                      ^      sandboxing
                      |      as a library)
                      |
        -----------------------------
        ^                           ^
        |                           |
        |                           |
     pinktrace                    GLib
     (Implements                  (Implements
      cross-platform               the required data structures;
      tracing functions)           like hashtables, linked lists etc.)


Let's see what the next days bring :-)
