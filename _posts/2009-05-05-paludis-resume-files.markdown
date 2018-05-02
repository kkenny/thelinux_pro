---
layout: post
title: Paludis Resume Files
categories: [en, blog]
tags: [paludis, zsh]
uuid: 19e5ad5c-b6a9-4d3b-9556-71d7cfd2c3e1
---

As many of you know [Paludis](http://paludis.pioto.org) has a
**--resume-command-template** option to save the resume command to a file.  
In addition to that there's the
[pretend-resume.hook](http://trac.pioto.org/paludis/browser/hooks/demos/pretend_resume.hook.in)
which displays the resume command  
or the file saved at the end of --pretend-install output.  
The only missing thing is a way to quickly execute this command prepending with
[sudo](http://www.sudo.ws/).  
I wrote a tiny [zsh](http://www.zsh.org/) function, which I called
[plast](http://github.com/alip/dotfiles/blob/master/zsh/functions/plast),  
to do the job. To use it, save the file somewhere in your **$fpath** and put

    export PALUDIS_RESUME_DIR=/path/to/the/directory/where/you/save/your/paludis/resume/command/files
    autoload -U plast

in your .zshrc. You can use it like:

    paludis -ip bla bla bla
    plast # executes the command in the newest resume file prepending with sudo
