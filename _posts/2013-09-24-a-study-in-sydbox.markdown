---
layout: post
title: A Study in Sydbox
categories: [en, blog]
tags: [sydbox, sydbox-1, ptrace, sandbox, sherlock holmes]
lang: en
uuid: db16f024-ee6c-4b89-83a8-ec7bdefd459b
---

Due to the fact that [sydbox][sydbox_1] is a low level tool which inspects
system calls, debugging its bugs become cumbersome at times. [GDB][gdb] and
[Valgrind][valgrind] are two valuable tools which comes to rescue.

I hit this bug when I was investigating [Exherbo bug 369][exherbo_bug_369]. I
wrote a small C program to reproduce the problem:

~~~ c
#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <elf.h>
#include <sys/auxv.h>
#include <sys/types.h>

int main(void)
{
    pid_t pid;
    int pfd[2];
    unsigned long val;
    char buf[1024];
    int auxfd;

    val = getauxval(AT_SECURE);
    fprintf(stderr, "getauxval(%lu) = %lu (errno:%d %s)\n",
        AT_SECURE, val, errno, strerror(errno));

    pipe(pfd);
    pid = fork();
    if (pid == 0) {
        /* 23 is AT_SECURE as defined in elf.h */
        char *const argv[] = {"sh", "-c", "od -t u8 | awk '{if ($2 == 23) print }'", NULL};
        close(pfd[1]);
        dup2(pfd[0], STDIN_FILENO);
        execvp(argv[0], argv);
    } else {
        close(pfd[0]);
        auxfd = open("/proc/self/auxv", O_RDONLY);
        while (read(auxfd, buf, 1024) > 0)
            write(pfd[1], buf, 1024);
        close(pfd[1]);
    }
}
~~~


I compiled this small program with [gcc][gcc] and when I run it under
[sydbox-1][sydbox_1] I witnessed an interesting output:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % ./sydbox ./a.out
getauxval(23) = 0 (errno:0 Success)
sydbox@1379972151: bash[26306.0:26305] sys:4|stat| PANIC_KILL
~~~

Note there is not a prompt at the end. [sydbox-1][sydbox_1] hung right after
logging `PANIC_KILL`. Before firing up a debugger and start to debug, let's
gather as much information as possible by checking whether [verbose
logging][verbose_logging] will tell us something:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % ./sydbox -m log/console_level:511 ./a.out
...
sydbox@1379972294: [wait(-1, 0x857f) = 28848] WIFSTOPPED,sig=133|(null)|
sydbox@1379972294: [wait(-1, 0x857f) = 28848] WIFSTOPPED,sig=133|(null)|
sydbox@1379972294: [wait(-1, 0x857f) = 28848] WIFSTOPPED,sig=133|(null)|
sydbox@1379972294: bash[28848.0:28847] sys:4|stat| entering system call
sydbox@1379972294: bash[28848.0:28847] sys:4|stat| PANIC_KILL
sydbox@1379972294: bash[28848.0:28847] sys:4|stat| trace_kill(sig:9) failed (errno:3|ESRCH| No such process)
sydbox@1379972294: process 28848 ignored
~~~

After a couple of `wait(2)` loops the `stat(2)` system call handler - which
takes [magic commands][magic_commands] as input paniced for some reason and
called the function `panic()` which decided to kill the traced process.

So far so good. Although this looks unrelated to the [bug at
hand][exherbo_bug_369], it is still a good idea to fix it when you have some
free time. Let's fire up the debugger and try to do a [reverse
debug][gdb_reverse_debugging]. I use [cgdb][cgdb] which provides a nice
curses frontend to [gdb][gdb].

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % libtool --mode=execute cgdb --args ./sydbox -m log/console_level:511 ./a.out
GNU gdb (GDB) 7.6.1
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-unknown-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /home/alip/src/sydbox/sydbox-1/src/.libs/lt-sydbox...done.
(gdb)
~~~

First let's break on `main()`, run the program and when the breakpoint is
hit set another breakpoint on `sys_stat` (the `stat(2)` system call handler
function) and start [recording][recording] the program instructions and `cont`inue.

~~~
(gdb) break main
Breakpoint 1 at 0x419d98: file sydbox.c, line 1255.
(gdb) run
Starting program: /home/alip/src/sydbox/sydbox-1/src/.libs/lt-sydbox -m log/console_level:511 ./a.out
warning: no loadable sections found in added symbol-file system-supplied DSO at
0x7ffff7ffa000
warning: Could not load shared library symbols for linux-vdso.so.1.
Do you need "set solib-search-path" or "set sysroot"?

Breakpoint 1, main (argc=4, argv=0x7fffffffd428) at sydbox.c:1255
(gdb) record
(gdb) break sys_stat
Breakpoint 2 at 0x411d58: file syscall-special.c, line 150.
(gdb) cont
Continuing.
Do you want to auto delete previous execution log entries when record/replay buffer becomes full (record full stop-at-limit)?([y] or n)
~~~

This takes some time. When the record/replay buffer is full, [gdb][gdb] kindly
asks you whether you want to continue execution and auto-delete previous log
entries or stop instantly and investigate further on. We're not interested in
the previous log entries so let's just hit `[enter]` and `cont`inue.

~~~
Process record and replay target doesn't support syscall number -1
Process record: failed to record execution log.

[process 8201] #1 stopped.
~~~

This is a weird message by [gdb][gdb] which fortunately I have seen before.
[sydbox-1][sydbox_1] makes use of some rather new system calls which [gdb][gdb]
does not support. The newest of those are `process_vm_readv` and
`process_vm_writev` which were added to Linux as of kernel version 3.2. I'll add
a small one-time tweak to the auto-generated `pinktrace/system.h` file telling
[sydbox-1][sydbox_1] that these system calls are not supported by the system and
let it use the good old `ptrace(2)` way of reading one `long` at a time:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % cd ../pinktrace
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % sed -i -e '/^#define PINK_HAVE_PROCESS_VM_\(READ\|WRITE\)V/s/1/0/' system.h
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % grep PINK_HAVE_PROCESS system.h
#define PINK_HAVE_PROCESS_VM_READV      0
#define PINK_HAVE_PROCESS_VM_WRITEV     0
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % make clean && make -j
~~~

Now let's return to `src/` and rebuild [sydbox][sydbox_1]:

    alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % cd ../src
    alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % make clean && make -j

Let's re-run [sydbox][sydbox_1] to make sure the bug is still there:

    alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % ./sydbox ./a.out
    getauxval(23) = 0 (errno:0 Success)
    0000340                   23                    0

This is where my luck kicks in! The bug is not there anymore. Now we know the
problem is actually in [pinktrace][pinktrace], the underlying library providing
thin wrappers around the `ptrace(2)` system call. We have also narrowed the
problem down to one of `process_vm_readv` and `process_vm_writev` functions. Now
let's go back to turn the `#define`s on and retry with [gdb][gdb]:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % cd ../pinktrace
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % sed -i -e '/^#define PINK_HAVE_PROCESS_VM_\(READ\|WRITE\)V/s/0/1/' system.h
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % grep PINK_HAVE_PROCESS system.h
#define PINK_HAVE_PROCESS_VM_READV      1
#define PINK_HAVE_PROCESS_VM_WRITEV     1
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % make clean && make -j
alip@hayalet ~/src/sydbox/sydbox-1/pinktrace (git)-[master] % cd ../src
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % make clean && make -j
~~~

Now we will start recording only after we enter the `sys_stat()` function:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % libtool --mode=execute cgdb --args ./sydbox -m log/console_level:511 ./a.out
GNU gdb (GDB) 7.6.1
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-unknown-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /home/alip/src/sydbox/sydbox-1/src/.libs/lt-sydbox...done.
(gdb) break sys_stat
Breakpoint 1 at 0x411d58: file syscall-special.c, line 150.
(gdb) run
...
sydbox@1379974050: [wait(-1, 0x857f) = 31387] WIFSTOPPED,sig=133|(null)|
sydbox@1379974050: [wait(-1, 0x857f) = 31387] WIFSTOPPED,sig=133|(null)|
sydbox@1379974050: bash[31387.0:31386] sys:4|stat| entering system call 

Breakpoint 1, sys_stat (current=0x62fa00) at syscall-special.c:150
(gdb) record
(gdb) cont
Continuing.
Process record and replay target doesn't support syscall number -1
Process record: failed to record execution log.

[process 31382] #1 stopped.
0x00007ffff78fa048 in process_vm_readv () from /usr/lib/libc.so.6
~~~

[Gdb][gdb] kindly stopped where the bug is actually located. Let's stop
recording and single-step to see what error this function returns.

~~~
(gdb) record stop
Process record is stopped and all execution logs are deleted.
(gdb) n
Single stepping until exit from function process_vm_readv, which has no line number information.
_pink_process_vm_readv (pid=31387, local_iov=0x7fffffffbe10, liovcnt=1, remote_iov=0x7fffffffbe00, riovcnt=1, flags=0) at vm.c:199
(gdb) n
(gdb) p r
$1 = -1
~~~

The function `_pink_process_vm_readv` is returning `-1` which is the negated
errno value `EPERM`. This makes `pink_vm_cread_nul` fail with -1 which in turn
makes `pink_read_vm_data_nul` return -1 which in turn makes `syd_read_string`
function to call `panic()`. Now we have a detailed information about the panic
happening.

Another valuable tool to aid in debugging system call inspection is
[strace][strace]. Let's check with strace what these `stat(2)` system calls'
arguments are. I have not updated my strace.git tree for a while and trying to
compile it I have found a problem due to an inconsistency between glibc and
linux kernel headers which [keruspe][keruspe] fixed for pinktrace with commit
[e1aa031][pinktrace_glibc_fix] a week ago:

~~~
alip@hayalet ~/src/strace (git)-[master] % make -j1
...
gcc -DHAVE_CONFIG_H -I.  -I./linux/x86_64 -I./linux -I./linux  -Wall -Wwrite-strings -D__ALIP_WAS_HERE -g -ggdb3 -O2 -march=native -D__PINK_IS_BEHIND_THE_WALL -MT process.o -MD -MP -MF .deps/process.Tpo -c -o process.o process.c
In file included from process.c:66:0:
/usr/include/linux/ptrace.h:58:8: hata: 'struct ptrace_peeksiginfo_args' yeniden tanımlanmış
 struct ptrace_peeksiginfo_args {
        ^
In file included from defs.h:169:0,
                 from process.c:37:
/usr/include/sys/ptrace.h:191:8: bilgi: originally defined here
 struct ptrace_peeksiginfo_args
        ^
~~~

`struct ptrace_peeksiginfo_args` is a recent addition to `ptrace.h` headers and
both `sys/ptrace.h` of [glibc-2.18][glibc_siginfo_commit] and `linux/ptrace.h`
of Linux define it. Thus defining the same struct twice fails. Fortunately we
have seen this error before with the [IA64 architecture][ia64] where the same
happens with `struct pt_all_user_regs` and `struct ia64_fpreg`.

Having hit another totally unrelated bug, I have prepared a patch and tested it:

~~~
alip@hayalet ~/src/strace (git)-[master] % make
gcc -Wall -Wwrite-strings -D__ALIP_WAS_HERE -g -ggdb3 -O2 -march=native -D__PINK_IS_BEHIND_THE_WALL   -o strace bjm.o block.o count.o desc.o file.o io.o ioctl.o ipc.o loop.o mem.o mtd.o net.o pathtrace.o process.o quota.o resource.o scsi.o signal.o sock.o strace.o stream.o syscall.o system.o term.o time.o util.o vsprintf.o  
make[2]: `/home/alip/src/strace' dizininden çıkılıyor
make[1]: `/home/alip/src/strace' dizininden çıkılıyor
~~~

It compiles and runs fine. Time to prepare a
[git-format-patch][git_format_patch] and send to strace-devel mailing list.
These git tools make it really easy to prepare patches and submit them. Here is
[the link to the actual mail][sourceforge_strace_devel_patch].

So far so good. Another bug fixed and submitted upstream. Let's go ahead and see
whether strace can make sense of those `stat(2)` arguments:

alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % ~/src/strace/strace -f -e stat ./a.out
Process 18698 attached
[pid 18697] +++ exited with 0 +++
stat(0x9db090, {...})                   = 0
stat(0x485897, {...})                   = 0
stat(0x485897, {...})                   = 0
...
~~~

Note the `-f` argument. Remember our panic line started with
`bash[31387.0:31386]` this does not happen in my small program but in bash which
is spawned right after `fork(2)`. The `-f` argument of [strace][strace] follows
forks.

Now the question is what those hex values in the first arguments are.
[strace][strace] usually does a good job in decoding strings so something is
weird going on here. Let's go one step ahead and try to trace [strace][strace]
using [strace][strace] itself. One has to be careful here not to use `-f` with
the first [strace][strace] because *only one process may trace a process at a
time* and we want the first [strace][strace] to only trace [strace][strace] not
our small program `a.out`. We also use the option `-e 'signal=!all'` so that we
filter some of the unwanted output:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % strace -q -e 'process_vm_readv' -e 'signal=!all' -- strace -e 'signal=!all' -f -e stat ./a.out
getauxval(23) = 0 (errno:0 Success)
Process 22286 attached
[pid 22285] +++ exited with 0 +++
process_vm_readv(22286, 0x7fff71faed40, 1, 0x7fff71faed50, 1, 0) = -1 EPERM (Operation not permitted)
stat(0x1938070, process_vm_readv(22286, 0x7fff71fafce0, 1, 0x7fff71fafcf0, 1, 0) = -1 EPERM (Operation not permitted)
{...})       = 0
~~~

The output of the two strace processes are mixed but here we can also see that
the system call `process_vm_readv()` returns the error condition `EPERM`.
Consulting the [process_vm_readv(2)][man_process_vm_readv] manual page:

~~~
EPERM  The caller does not have permission to access the address space of the process pid.
~~~

Now, why on earth is `ptrace()` is permitted but `process_vm_readv()` is not? It
is clear that they are two different APIs. It is time to dig into the kernel
source. Having walked through the kernel code on [lxr][lxr] for a while, I
figured this [sydbox-1][sydbox_1] PANIC was due to the fact that I have the
sysctl `kernel.yama.ptrace_scope` set to 1 which is [YAMA restricting
ptrace()][yama_restricts_ptrace]. After:

~~~
alip@hayalet ~/src/sydbox/sydbox-1/src (git)-[master] % sudo sysctl kernel.yama.ptrace_scope=0
kernel.yama.ptrace_scope = 0
~~~

Everything works OK and now I am aware of the fact that there is another way to
restrict `ptrace()` and I will work on [sydbox-1][sydbox_1] to make it handle
such errors gracefully (without hanging) but that's for another night.

Confession: I started working at [Özgür Yazılım A.Ş.][ozgur_yazilim] as a Linux
system administrator and programmer and I have been using [Arch
Linux][arch_linux] for a while which means I have not been configuring/compiling
my own kernel. This was a nice message to me that I should stop being a slacker
and return to [Exherbo][exherbo] now.

The [Exherbo bug 369][exherbo_bug_369] is still not fixed, but I am working on
it :-)

[sydbox_1]: http://git.exherbo.org/sydbox-1.git/
[gdb]: http://www.sourceware.org/gdb/
[valgrind]: http://valgrind.org/
[gcc]: http://gcc.gnu.org/
[strace]: http://sourceforge.net/projects/strace/
[exherbo_bug_369]: https://bugs.exherbo.org/show_bug.cgi?id=369
[keruspe]: http://www.imagination-land.org/
[pinktrace_glibc_fix]: http://git.exherbo.org/sydbox-1.git/commit/?id=e1aa0310946cd4c36259485d67804fb24fd79278
[glibc_siginfo_commit]: http://www.sourceware.org/git/?p=glibc.git;a=commit;h=521c6785e1fc94d1f501743e9a40af9e02797df3
[sourceforge_strace_devel_patch]: http://sourceforge.net/p/strace/mailman/message/31441642/
[lxr]: http://lxr.linux.no/
[linux_fs_exec_c]: http://lxr.linux.no/#linux+v3.11.1/fs/exec.c#L1665
[yama_restricts_ptrace]: http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=2d514487faf188938a4ee4fb3464eeecfbdcf8eb
[ia64]: http://en.wikipedia.org/wiki/Itanium
[man_process_vm_readv]: http://man7.org/linux/man-pages/man2/process_vm_readv.2.html
[arch_linux]: https://www.archlinux.org/
[exherbo]: http://www.exherbo.org/
[ozgur_yazilim]: http://www.ozguryazilim.com.tr/
[pinktrace]: http://git.exherbo.org/sydbox-1.git/tree/pinktrace
[verbose_logging]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#logging
[git_format_patch]: https://www.kernel.org/pub/software/scm/git/docs/git-format-patch.html
[cgdb]: http://cgdb.github.io/
[magic_commands]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#configuration
[gdb_reverse_debugging]: http://www.gnu.org/s/gdb/news/reversible.html
