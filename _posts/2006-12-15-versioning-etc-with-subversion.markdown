---
layout: post
title: Versioning /etc with Subversion
categories: [en, blog]
uuid: d9002275-0c8b-4887-b6eb-cb5ce04e359e
---

Although Portage takes care of configuration files very well, no system can have  
enough protection from human errors. Versioning configuration files under __/etc__  
is a nice solution to this. If you do a mistake and delete some file or any  
other silliness that might happen, you just revert to a former revision and  
solve the problem.

This can be achieved easily:

    # First create a subversion repository:
    $ svnadmin create /root/svn
    # Then import /etc to the repository:
    $ svn import /etc file:///root/svn -m 'Initial import'
    # Checkout the project:
    $ rm -fr /etc
    $ svn ci file:///root/svn/etc

Now change some configuration files and do __svn status__ . When you change your  
configuration files, you can commit them to the repository:

    cd /etc
    svn ci -m 'Changed MAKEOPTS to -j2 in /etc/make.conf'

Linux rulez!
