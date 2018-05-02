---
layout: post
title: Doxygen and Git
categories: [en, blog]
tags: [doxygen, git]
uuid: 5f397db2-5d21-4b82-afdd-b021aa031cf1
---

If you have a project using [Doxygen](http://www.doxygen.org/) for documentation
and [Git](http://git-scm.com/) for source control management you may use this
trick in `doxygen.conf`:

    FILE_VERSION_FILTER = "/bin/sh -c 'git log --pretty=\"format:%ci\" -1 \"${1}\" || echo no git'"

This will show date of the last commit in the header:

![simple](/images/2010-12-14-doxygen-git/simple.png "Simple date with Doxygen and Git")

You can give even more useful information using git's pretty formats:

    FILE_VERSION_FILTER = "/bin/sh -c 'git log --pretty=\"format:%ci, author:%aN <%aE>, commit:%h\" -1 \"${1}\" || echo no git'"

This looks like:

![detailed](/images/2010-12-14-doxygen-git/detailed.png "Detailed information with Doxygen and Git")

Note this may vastly increase runtime of [Doxygen](http://www.doxygen.org/) if
you have lots of files to process, but I think it is a nice way to give
information to project users.
