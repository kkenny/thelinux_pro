---
layout: post
title: Killing tracees on exit with sydbox-1
categories: [en, blog]
tags: [sydbox, sydbox-1, ptrace, sandbox]
lang: en
uuid: 0ad69867-2437-47f9-98de-306d189eabbe
---

As I've written in my blog post [Recent Linux changes to help
sandboxing][recent_changes]
Linux has a few new features which may aid in enhancing sydbox-1.

One of these features is `PTRACE_O_EXITKILL`. This is a new ptrace option to
kill tracees upon tracer exit. Quoting from [ptrace(2)][man_ptrace]

    PTRACE_O_EXITKILL (since Linux 3.8)
    If a tracer sets this flag, a SIGKILL signal will be sent to every
    tracee if the tracer exits.  This option is useful for ptrace
    jailers  that want to ensure that tracees can never escape the
    tracer's control.

This is a simple feature providing a nice enhancement. [sydbox-1][sydbox_1] had
a similar feature to prevent tracees from running upon an abnormal exit.  There
are two options, namely [core/abort/decision][core_abort_decision] and
[core/panic/decision][core_panic_decision], which when given the value `killall`
sends `SIGKILL` to all traced processes upon abnormal exit. There is also the
option [core/trace/exit_wait_all][core_trace_exit_wait_all] to make
[sydbox-1][sydbox_1] wait for all tracees to exit before exiting.

However, doing this in user-space is tricky and error-prone. Considering it's
the *tracer* who is dying *unexpectedly*, it may not always be possible to kill
tracees which will then run in potentially unsafe mode. You can read this [lkml
thread][lkml_exitkill] and many more to dive into the internals of `ptrace(2)`.

Thus, [sydbox-1][sydbox_1] learned a new [magic command][sydbox_1_configuration]
with the name [core/trace/exit_kill][core_trace_exit_kill] to turn this
functionality on with the two commits I pushed to master today:

* [pinktrace: new option PINK_TRACE_OPTION_EXITKILL][pinktrace_exitkill]
* [New magic command core/trace/exit_kill][sydbox_exitkill]

One restriction is the option [core/trace/exit_kill][core_trace_exit_kill] is
only useful when it is set upon startup. It does **not** work with the [magic
stat() system call][sydbox_1_configuration]. `ptrace(2)` options are inherited
from parent to children thus trying to set this on a per-tracee basis requires
one to change the value of the option for the parent and *all* its children.
Although this is possible in theory ([sydbox-1][sydbox_1] keeps track of
parent<->children relationships) it would add some complexity to the program
which I do not want unless I see a well-founded reason to do so.

[recent_changes]: /en/blog/2013/02/22/recent-linux-changes-help-sandboxing/
[man_ptrace]: http://linux.die.net/man/2/ptrace
[sydbox_1]: http://git.exherbo.org/sydbox-1.git/
[core_abort_decision]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#core-abort-decision
[core_panic_decision]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#core-panic-decision
[core_trace_exit_wait_all]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#core-trace-exit_wait_all
[core_trace_exit_kill]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#core-trace-exit_kill
[lkml_exitkill]: http://article.gmane.org/gmane.linux.kernel/1390167
[sydbox_1_configuration]: http://dev.exherbo.org/~alip/sydbox/sydbox.html#configuration
[pinktrace_exitkill]: http://git.exherbo.org/sydbox-1.git/commit/?id=a1fc5bafdae976f4a8ed7a9bef7876be6eceb65d
[sydbox_exitkill]: http://git.exherbo.org/sydbox-1.git/commit/?id=cb9bcdbf92d36c7078dd7267faa2fcc21a9d789b
