---
layout: post
title: Sandboxing Skype with sydbox-1
categories: [en, blog]
tags: [sydbox, sydbox-1, skype, sandbox, security, apparmor, tomoyo, selinux, grsecurity, exherbo, arch]
lang: en
uuid: d857ea22-5632-4204-9bb5-c54246a640da
---

There are various tools to provide enhanced restriction mechanisms under
[Linux][linux]. In case security is the major concern, these mechanisms need to
be in the kernel level which in turn means specific configurations or in some
cases modifications (in forms of patches etc.) to the [Linux kernel][linux].
Some examples are [AppArmor][apparmor], [Security Enhanced Linux][selinux],
[Tomoyo Linux][tomoyo], and [Grsecurity][grsec]. User space solutions are
either not as flexible or not as secure depending on the use case scenario.

We, at [Exherbo][exherbo], need a sandbox for misbehaving package builds.  One
should note that such misbehaviours can sometimes be rather fun (or [not safe
for work][nsfw] at times). I used the term *misbehaving* on purpose because
this does not mean the sandbox itself can make the build environment *totally
secure*. Linux has good old [UNIX][unix] goodies like [separate permissions for
users][privsep], [chroots][chroot] and new shiny stuff like [per-process
namespaces][namespaces] to implement further restrictions.

[Exherbo][exherbo]'s practical solution to this issue is [sydbox][sydbox-1]. With
the upcoming version [sydbox-1][sydbox-1] - which is yet to be released - this
solution can easily be adapted to different use cases.

As I was browsing through [Arch Linux Wiki][archwiki] pages I stumbled upon the
[Skype][skype-arch] page which describes different approaches to restrict such
close sourced applications.

I am not claiming using [sydbox-1][sydbox-1] for this purpose is secure but it
is most certainly practical. Here is my proof-of-concept attempt at sandboxing
[Skype][skype] using [sydbox-1][sydbox-1]. Below is a sample
[sydbox-1 profile][skype-profile] for use with [Skype][skype]. You can also
find it in [sydbox-1.git][sydbox-1.git] under <tt>examples/</tt> directory.

    # sydbox profile for Skype4

    #
    # Sandboxing
    #
    core/sandbox/exec:deny
    core/sandbox/read:deny
    core/sandbox/write:deny
    core/sandbox/network:deny

    core/whitelist/per_process_directories:true
    core/whitelist/successful_bind:true
    core/whitelist/unsupported_socket_families:true

    core/abort/decision:killall
    core/panic/decision:kill
    core/panic/exit_code:-1
    core/violation/decision:deny
    core/violation/exit_code:-1
    core/violation/raise_fail:false
    core/violation/raise_safe:false

    core/trace/follow_fork:true
    core/trace/exit_wait_all:true
    core/trace/magic_lock:off
    core/trace/interrupt:while_wait
    core/trace/use_seccomp:true
    core/trace/use_seize:true
    core/trace/use_toolong_hack:true

    core/match/case_sensitive:true
    core/match/no_wildcard:literal

    #
    # Logging
    #
    log/file:
    log/level:511
    log/console_fd:2
    log/console_level:3

    #
    # /dev
    #
    whitelist/read+/dev
    whitelist/read+/dev/urandom
    whitelist/read+/dev/stdout
    whitelist/read+/dev/stderr
    whitelist/write+/dev/tty*
    whitelist/write+/dev/pts/***
    whitelist/read+/dev/snd/***
    whitelist/write+/dev/snd/***
    whitelist/read+/dev/video*
    whitelist/write+/dev/video*

    #
    # /proc & /sys
    #
    whitelist/read+/proc/cpuinfo
    whitelist/read+/proc/meminfo
    whitelist/read+/proc/stat
    whitelist/read+/proc/net
    whitelist/read+/proc/net/arp
    whitelist/read+/proc/net/route
    whitelist/read+/proc/net/unix
    whitelist/read+/proc/sys/vm/overcommit_memory
    whitelist/read+/proc/sys/kernel/osrelease
    whitelist/read+/proc/sys/kernel/ostype
    whitelist/read+/sys/devices/system/cpu/online
    whitelist/read+/sys/devices/system/cpu
    whitelist/read+/sys/devices/system/cpu/cpu?/cpufreq/scaling_cur_freq
    whitelist/read+/sys/devices/system/cpu/cpu?/cpufreq/scaling_max_freq
    whitelist/read+/sys/devices/virtual/dmi/id/board_name
    whitelist/read+/sys/devices/virtual/dmi/id/board_version
    whitelist/read+/sys/devices/virtual/dmi/id/board_vendor
    whitelist/read+/sys/devices/virtual/dmi/id/product_name
    whitelist/read+/sys/devices/virtual/dmi/id/product_version
    whitelist/read+/sys/devices/virtual/dmi/id/sys_vendor
    whitelist/read+/sys/devices/*/*/*/power_supply/ACAD/***
    whitelist/read+/sys/devices/*/*/*/*/*/*/modalias
    whitelist/read+/sys/devices/*/*/*/*/*/*/video4linux/video?/dev
    whitelist/read+/sys/devices/*/*/*/*/*/idProduct
    whitelist/read+/sys/devices/*/*/*/*/*/idVendor
    whitelist/read+/sys/devices/*/*/*/*/*/speed

    #
    # nscd (glibc)
    #
    whitelist/network/connect+unix:/var/run/nscd/socket
    whitelist/network/connect+unix:/run/nscd/socket

    #
    # /etc
    #
    whitelist/read+/etc/asound.conf
    whitelist/read+/etc/group
    whitelist/read+/etc/hosts
    whitelist/read+/etc/host.conf
    whitelist/read+/etc/ld.so.cache
    whitelist/read+/etc/ld.so.preload
    whitelist/read+/etc/nsswitch.conf
    whitelist/read+/etc/resolv.conf
    whitelist/read+/etc/ssl/certs/***
    whitelist/read+/etc/fonts/***
    whitelist/read+/etc/gtk-2.0/***
    whitelist/read+/etc/pango/***

    #
    # Libraries
    #
    whitelist/read+/lib*/***
    whitelist/read+/usr/lib*/***

    #
    # Share dirs
    #
    whitelist/read+/usr/share/alsa/***
    whitelist/read+/usr/share/ca-certificates/***
    whitelist/read+/usr/share/locale/***
    whitelist/read+/usr/share/zoneinfo/***
    whitelist/read+/usr/share/fonts/***
    whitelist/read+/usr/share/icons/***
    whitelist/read+/usr/share/pixmaps/***
    whitelist/read+/usr/share/texmf-dist/fonts/***
    whitelist/read+/usr/share/X11/***

    #
    # Xorg/X11 & dbus
    #
    whitelist/network/connect+unix-abstract:/tmp/.X11-unix/**
    whitelist/network/connect+unix-abstract:/tmp/.ICE-unix/**
    whitelist/network/connect+unix-abstract:/tmp/dbus-*
    whitelist/network/connect+unix:/run/dbus/system_bus_socket
    whitelist/network/connect+unix:/var/run/dbus/system_bus_socket

    #
    # /tmp
    #
    whitelist/read+/tmp/qtsingleapp-*
    whitelist/write+/tmp/qtsingleapp-*
    whitelist/network/bind+unix:/tmp/qtsingleapp-*
    whitelist/network/connect+unix:/tmp/qtsingleapp-*

    #
    # Skype
    #
    whitelist/read+/etc/Skype.conf
    whitelist/read+/etc/Skype/***
    whitelist/read+/usr/*bin/skype
    whitelist/exec+/usr/*bin/skype
    whitelist/exec+/usr/lib*/skype/skype
    whitelist/exec+/opt/skype/skype
    whitelist/read+/opt/skype/***
    whitelist/read+/usr/share/skype/***

    #
    # Host specific configuration under /home
    #
    whitelist/read+/home/*/.Xauthority
    whitelist/read+/home/*/.ICEauthority
    whitelist/read+/home/*/.gtkrc*
    whitelist/read+/home/*/.config/Trolltech.conf
    whitelist/write+/home/*/.icons/***

    #
    # Skype specific configuration
    #
    whitelist/read+/home/*/.asoundrc
    whitelist/read+/home/*/.config/Skype/***
    whitelist/write+/home/*/.config/Skype/***
    whitelist/read+/home/*/.Skype/***
    whitelist/write+/home/*/.Skype/***

    #
    # Temporary files & caches
    #
    whitelist/read+/home/*/.cache/fontconfig/***
    whitelist/write+/home/*/.cache/fontconfig/***
    whitelist/read+/home/*/.compose-cache/***
    whitelist/write+/home/*/.compose-cache/***

    #
    # Networking
    #
    # note: allow IPv4 and IPv6 by default since Skype operates on a P2P model.
    # You may further restrict access by only allowing access to SKYPENET,
    # Akamai and Microsoft Corporation together with your contact's IP
    # address.
    #
    whitelist/network/bind+LOOPBACK@0
    whitelist/network/connect+inet:0.0.0.0/0@0-65000
    whitelist/network/connect+inet6:::0/0@0-65000

    #
    # Allow some external programs
    #
    whitelist/exec+/usr/*bin/xdg-open
    exec/resume_if_match+/usr/*bin/xdg-open

A couple of things to note:

1. [sydbox-1][sydbox-1] is still in heavy development and the file format may
    change.
2. This approach is **not** secure. Author claims no responsibility if
    [Skype][skype] kills your [goats][goat].
3. [Three is the loneliest number since number two which is the loneliest number since
   the number one.][loneliest]

Happy hacking!

[apparmor]: http://wiki.apparmor.net/index.php/Main_Page
[archwiki]: https://wiki.archlinux.org/
[chroot]: http://en.wikipedia.org/wiki/Chroot
[exherbo]: http://www.exherbo.org/
[grsec]: http://grsecurity.net/
[goat]: http://dev.exherbo.org/~alip/images/goat-robs-car.jpg
[linux]: http://www.kernel.org/
[loneliest]: http://www.youtube.com/watch?v=22QYriWAF-U
[namespaces]: https://lwn.net/Articles/531114/
[nsfw]: https://bugs.gentoo.org/show_bug.cgi?id=298150
[privsep]: http://en.wikipedia.org/wiki/Privilege_separation
[selinux]: http://selinuxproject.org/
[skype]: http://www.skype.com/
[skype-arch]: https://wiki.archlinux.org/index.php/Skype
[skype-profile]: http://git.exherbo.org/sydbox-1.git/tree/examples/skype.syd-1
[sydbox-1]: http://git.exherbo.org/sydbox-1.git/
[sydbox-1.git]: git://git.exherbo.org/sydbox-1.git
[tomoyo]: http://tomoyo.sourceforge.net/
[unix]: http://en.wikipedia.org/wiki/Unix
