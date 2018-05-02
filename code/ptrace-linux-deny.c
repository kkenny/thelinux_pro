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

#if defined(__i386__)
#define ORIG_ACCUM	(4 * ORIG_EAX)
#elif defined(__x86_64__)
#define ORIG_ACCUM	(8 * ORIG_RAX)
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
