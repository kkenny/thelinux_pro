---
layout: post
title: ptrace on BSD
categories: [en, blog]
tags: [bsd, ptrace, sydbox]
uuid: 10acfb37-350b-4599-9290-45b17f62ccbd
---

`ptrace` is a system call which is used for process tracing
and debugging. This system call is available on many operating systems.
However each operating system has different versions.

I want to explain about my efforts to port
[sydbox](http://projects.0x90.dk/projects/show/sydbox) to
[FreeBSD](http://www.freebsd.org/). The
[ptrace implementation](http://www.freebsd.org/cgi/man.cgi?query=ptrace&apropos=0&sektion=0&manpath=FreeBSD+8.0-RELEASE&format=html)
of [FreeBSD](http://www.freebsd.org/) is similar to
[Linux](http://www.kernel.org/)'. The request
`PT_SYSCALL` is available to stop the traced process at every system call and
exit similar to `PTRACE_SYSCALL` of [Linux](http://www.kernel.org/).
In addition to that [FreeBSD](http://www.freebsd.org/) has the requests
`PT_TO_SCE` and `PT_TO_SCX` which stops the traced process **only** at the
beginning of system call entry or exit.  This is a feature I really miss on
Linux.

There is, however, a big difference, I'm inclined to call it a bug, about
`ptrace` on [FreeBSD](http://www.freebsd.org/). When a traced process is stopped
at the entry of a system call, there's no way to prevent the execution of this
system call. On Linux this is done by changing the system call number to either
something invalid like `0xbadca11` or something harmless like `getpid`.

[Here](/code/ptrace-linux-deny.c) is an example:

{% highlight c %}

    /* denying system calls using ptrace on Linux
     */

    #include <assert.h>
    #include <fcntl.h>
    #include <signal.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <sys/reg.h>
    #include <sys/types.h>
    #include <sys/wait.h>
    #include <sys/ptrace.h>
    #include <linux/ptrace.h>

    #if defined(__x86__)
    #define ORIG_ACCUM    (4 * ORIG_EAX)
    #elif defined(__x86_64__)
    #define ORIG_ACCUM    (8 * ORIG_RAX)
    #else
    #error unsupported architecture
    #endif

    int main(void)
    {
            int status;
            pid_t pid;

            if ((pid = fork()) < 0) {
                    perror("fork");
                    abort();
            }
            else if (pid == 0) {
                    ptrace(PTRACE_TRACEME, 0, NULL, NULL);
                    kill(getpid(), SIGSTOP);
                    open("foo.bar", O_WRONLY | O_CREAT);
                    _exit(0);
            }

            if (waitpid(pid, &status, 0) < 0) {
                    perror("waitpid");
                    abort();
            }

            assert(WIFSTOPPED(status));
            assert(WSTOPSIG(status) == SIGSTOP);

            if (ptrace(PTRACE_SYSCALL, pid, NULL, NULL) < 0) {
                    perror("ptrace(PTRACE_SYSCALL, ...)");
                    ptrace(PTRACE_KILL, pid, NULL, NULL);
                    abort();
            }

            if (waitpid(pid, &status, 0) < 0) {
                    perror("waitpid");
                    ptrace(PTRACE_KILL, pid, NULL, NULL);
                    abort();
            }

            assert(WIFSTOPPED(status));
            assert(WSTOPSIG(status) == SIGTRAP);

            /* Change the system call to something invalid, so it will be denied.
             */
            if (ptrace(PTRACE_POKEUSER, pid, ORIG_ACCUM, 0xbadca11) < 0) {
                    perror("ptrace(PTRACE_POKEUSER, ...)");
                    ptrace(PTRACE_KILL, pid, NULL, NULL);
                    abort();
            }

            /* Let the process continue */
            ptrace(PTRACE_CONT, pid, NULL, NULL);

            waitpid(pid, &status, 0);
            assert(WIFEXITED(status));
            exit(WEXITSTATUS(status));
    }

{% endhighlight %}

<!-- _ -->

Now although the traced process calls `open("foo.bar", O_WRONLY | O_CREAT)`
the file `foo.bar` won't be created because the tracer process denies the system
call.

[Here](/code/ptrace-freebsd-deny.c) is the same example for
[FreeBSD](http://www.freebsd.org/):

{% highlight c %}

    /* denying system calls using ptrace on FreeBSD
     */

    #include <assert.h>
    #include <fcntl.h>
    #include <signal.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <sys/types.h>
    #include <sys/wait.h>
    #include <sys/ptrace.h>
    #include <machine/reg.h>

    int main(void)
    {
            int status;
            pid_t pid;
            struct reg r;

            if ((pid = fork()) < 0) {
                    perror("fork");
                    abort();
            }
            else if (pid == 0) {
                    ptrace(PT_TRACE_ME, 0, NULL, 0);
                    kill(getpid(), SIGSTOP);
                    open("foo.bar", O_WRONLY | O_CREAT);
                    _exit(0);
            }

            if (waitpid(pid, &status, 0) < 0) {
                    perror("waitpid");
                    abort();
            }

            assert(WIFSTOPPED(status));
            assert(WSTOPSIG(status) == SIGSTOP);

            if (ptrace(PT_SYSCALL, pid, (caddr_t)1, 0) < 0) {
                    perror("ptrace(PT_SYSCALL, ...)");
                    ptrace(PT_KILL, pid, (caddr_t)1, 0);
                    abort();
            }

            if (waitpid(pid, &status, 0) < 0) {
                    perror("waitpid");
                    ptrace(PT_KILL, pid, (caddr_t)1, 0);
                    abort();
            }

            assert(WIFSTOPPED(status));
            assert(WSTOPSIG(status) == SIGTRAP);

            /* Change the system call to something invalid, so it will be denied.
             */
            if (ptrace(PT_GETREGS, pid, (caddr_t)&r, 0) < 0) {
                    perror("ptrace(PT_GETREGS, ...)");
                    ptrace(PT_KILL, pid, (caddr_t)1, 0);
                    abort();
            }

            r.r_eax = 0xbadca11;

            if (ptrace(PT_SETREGS, pid, (caddr_t)&r, 0) < 0) {
                    perror("ptrace(PT_SETREGS, ...)");
                    ptrace(PT_KILL, pid, (caddr_t)1, 0);
                    abort();
            }

            /* Let the process continue */
            ptrace(PT_CONTINUE, pid, (caddr_t)1, 0);

            exit(0);
    }

{% endhighlight %}

<!-- _ -->

We expect the same to happen here, the file `foo.bar` shouldn't be created.
But it's created. Replace the `PT_GETREGS` and `PT_SETREGS` calls with a
`PT_KILL` to terminate process with signal `SIGKILL`. The file will still
be created! So there's no way to deny a system call using `ptrace` which makes
it impossible to port [sydbox](http://projects.0x90.dk/projects/show/sydbox) to
[FreeBSD](http://www.freebsd.org/) without patching the kernel.

None of the other BSD's, neither
[NetBSD](http://netbsd.gw.com/cgi-bin/man-cgi?ptrace++NetBSD-current) nor
[DragonFlyBSD](http://leaf.dragonflybsd.org/cgi/web-man?command=ptrace&section=2) nor
[OpenBSD](http://www.openbsd.org/cgi-bin/man.cgi?query=ptrace&sektion=2&format=html),
has the ptrace request `PT_SYSCALL` so I haven't checked if the behaviour is the
same on these systems.
