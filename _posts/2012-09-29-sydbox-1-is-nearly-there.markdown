---
layout: post
title: sydbox-1 is nearly there
categories: [en, blog]
tags: [sydbox, sydbox-1, seccomp]
uuid: fc53288c-2827-46ef-ae43-89a27fe283c1
---

After nearly two years I began working on a sydbox replacement[^1] she is
finally nearing completion. This post is meant both as a preliminary
announcement and help request.

sydbox-1 has been in ::arbor for sometime as sydbox-scm[^2] and paludis
supports it since version
[0.78.1](http://ciaranm.wordpress.com/2012/08/13/paludis-0-78-1-released/).
The git repository is hosted on exherbo.org[^3]. Before going on to tell you about
her I want to kindly ask you to help me with some tasks:

- Proof read the manual page[^4]. I am still unsure about the configuration
  file format and the magic command API so now is the time to share your
  ideas and views to help make sydbox-1 better.

- For brave souls, unmask it and install it. Especially important is to
  run its tests. To do that you have to set the environment variable
  PALUDIS\_DO\_NOTHING\_SANDBOXY[^5]. You will notice that it doesn't depend
  on pinktrace anymore. This is because sydbox-1 includes a rewrite of
  pinktrace which will eventually be released as pinktrace-1.

- Once again for brave souls, use it on your system. I am especially
  interested in how it performs during the `src_test` phase of
  exhereseses so please make sure tests are enabled if you do so and
  report back any issues (accompanied with a poem of your choosing!).
  It is always a good idea to have a pbin of the package in question
  to easily rollback changes in case you hit a severe bug[^6].

If you are bored, you can stop reading now. I will go on to introduce
sydbox-1.

### Why?
I am not a professional programmer. However, I have gained many
experiences after writing sydbox-0 and watching it perform as the
default sandbox of Exherbo. sydbox-0 has many shortcomings and drawbacks
which made it rather hard to maintain. Such as:

- sydbox-0 was based on the now unmaintained `catbox` initially.
  There are many design issues which didn't fit with our use
  cases for Exherbo.
- Being GPL-2 licensed it was problematic to share code with
  the well-established `ptrace(2)` based projects like `strace`
  and `truss` (of FreeBSD). I have partially solved this problem
  by writing pinktrace - a BSD3 licensed library providing thin
  wrappers around certain `ptrace(2)` calls but this was not
  enough. (See below about `pinktrace-easy`)
- Being a crucial part of the system set, dependencies like
  `GLib` was obviously a bad idea.
- Over the years as sydbox-0 codebase grew there were unforeseen
  code maintenance problems making it difficult to add new
  features.

### Features of sydbox-1

Below are main features of sydbox-1. You may consult the manual page³
for more information.

- No external dependencies. `GLib` dependency is gone for good
  among with the ini-format configuration file. sydbox-1 uses
  JSON format for configuration.
- Most of the `ptrace(2)` work is now abstracted by a
  callback-driven higher-level BSD3 licensed library called
  `pinktrace-easy`. This makes both the maintenance easier and
  code sharing with `strace` less problematic.
- Well designed, well documented magic command API which fits in
  with the configuration file format and provides an easier
  experience during command line invocation.
- Process dump can be obtained by sending sydbox-1 the `SIGUSR1`
  signal (or `SIGUSR2` for a more verbose dump). This makes it
  easier to debug sydbox hangs.
- Better signal handling to make sydbox more immune to
  interrupts.
- More powerful and configurable rsync-like pattern matching.
- Support for secure computing mode aka seccomp[^7]. This requires
  Linux-3.5 or newer and `CONFIG_SECCOMP=y` and
  `CONFIG_SECCOMP_FILTER=y` kernel configuration options. sydbox-scm
  exheres has a seccomp option to pass `--enable-seccomp` to
  econf. This is one of the key features which may make sydbox-1
  faster compared to sydbox-0 because in this mode sydbox only
  traces the sandboxed system calls. Tracing other commonly used
  system calls - think threaded applications calling
  sched\_yield() - is therefore avoided.
- Logging is easier to filter. This still needs some work
  though.
- Port numbers can now be entered as service names which will be
  queried from the `services(5)` database.
- Unsupported socket families can be whitelisted/blacklisted.
- New magic commands exec/resume\_if\_match and
  exec/kill\_if\_match are added. These commands may be used to
  resume or kill matching binaries upon successful execution.
  Paludis has `esandbox resume` and `esandbox kill` commands as
  an interface for exheres-0 (Make sure `esandbox api` returns 1
  before using them). See systemd.exlib as an example on
  how we can now restart services from within exhereseses
  without worrying about sandboxing.
- Read sandboxing to prevent unwanted filesytem reads.
- Black listing is now also supported in addition to
  white listing. This may be used to make an "allow by default
  and black list unwanted accesses" sandboxing policy.
- Many bugs fixed, some new system calls are sandboxed.

### How can I thank you?

Send me poems[^8]!

[^1]: She used to be called `pandora` in the early days.
[^2]: Not sydbox-0-scm which is the old one.
[^3]: <http://git.exherbo.org/sydbox-1.git/>
[^4]: <http://dev.exherbo.org/~alip/sydbox/sydbox.html>
[^5]: Eventually sydbox-1 will install its tests so this phase is going to
   be more convenient.
[^6]: sydbox-1 has been tested for some time by kind people and I have
     heard about only one such issue so far but it is always a good idea
     to be cautious.
[^7]: <http://lwn.net/Articles/475043/>
[^8]: <http://dev.exherbo.org/~alip/sydbox/poems.txt>
