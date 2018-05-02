---
layout: post
title: "vim script: hints_man3"
categories: [en, blog]
tags: [man, script, vim]
uuid: 6f879705-b5c0-44cb-bfef-dff9905bc4cb
---

I found a new vim script called
[hints\_man3](http://www.vim.org/scripts/script.php?script_id=1826).  
It shows the prototype of C library functions as you write them.  
You need to set your <tt>cmdheight</tt> option to at least 2 for it to work.  
This can be done by adding:

    au BufRead,BufNewFile *.c,*.h set ch=2

to your .vimrc file. Here's a screenshot:  
![hints\_man3](/images/hints_man3.png "hints_man3 screenshot")
