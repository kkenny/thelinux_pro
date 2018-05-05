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
