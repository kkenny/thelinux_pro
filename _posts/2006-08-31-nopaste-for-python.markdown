---
layout: post
title: Nopaste for Python
categories: [en, blog]
tags: [nopaste, python]
uuid: c4436212-40a7-4df9-bbe3-f7899a8a4e92
---

Today I rewrote
[app-text/nopaste](http://packages.gentoo.org/package/app-text/nopaste) with
[Python](http://www.python.org).  
It's a simple command line interface to [rafb.net/paste](http://rafb.net/paste).  
I don't want to install [Ruby](http://www.ruby-lang.org) just for that small script.  
In addition to that [Python](http://www.python.org) is a more appropriate
language than [Ruby](http://www.ruby-lang.org). ;)

Simple usage:

    hawking@localhost ~/python/nopaste $ ./nopaste.py -h
    nopaste script for rafb.net/paste
    usage : nopaste.py [options]
    Options:
        -h,--help        You're looking at it
        -l,--language    Set language ( defaults to 'Plain Text')
        -n,--nick        nickname
        -d,--desc        description
        -v,--verbose     verbose mode
        -c,--nocolor     supress coloring of output
        -x               Nopaste from X selection instead of stdin
                         (using xclip or xcut)

You can specify a http proxy by setting the **http\_proxy** environment variable.

    hawking@localhost ~/python/nopaste $ export http_proxy=http://127.0.0.1:8118
    hawking@localhost ~/python/nopaste $ cat test.py | ./nopaste.py -l Python -n hawking -d "a nice python script" -v
    Verbose mode
    Language :   Python
    Nick     :   hawking
    Description :   a nice python script
    Setting headers
    Encoding parameters
    Sending the request
    Reading...
    http://www.rafb.net/paste/results/rzH00g32.html
    hawking@localhost ~/python/nopaste $

You can get the script [here](/code/nopaste.py).
