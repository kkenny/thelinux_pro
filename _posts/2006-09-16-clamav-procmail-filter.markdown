---
layout: post
title: ClamAV Procmail Filter
categories: [en, blog]
tags: [python, clamav, procmail]
uuid: e3e51e31-7398-4d63-89c3-b8860651d39c
---

I wrote a simple filter for [procmail](http://www.procmail.org/) to scan mails
with [ClamAV](http://www.clamav.net/).  
By default clamd has a socket file under __/var/run/clamav/clamd.sock__ and  
this filter connects to it and gets the mail scanned.  
It adds a __X-CLAMAV__ header to the email to inform the reader.  
[Here](/code/clamdfilter.py) is the script.
