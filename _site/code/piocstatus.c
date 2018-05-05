/* vim: set cino= fo=croql sw=8 ts=8 sts=0 noet cin fdm=syntax : */

#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#include <sys/ioctl.h>
#include <sys/pioctl.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
	int pfd, status;
	pid_t pid;
	char proc[32];
	struct procfs_status ps;

	if ((pid = fork()) < 0) {
		perror("fork");
		return 1;
	}
	else if (!pid) {
		ptrace(PT_TRACE_ME, 0, NULL, 0);
		kill(getpid(), SIGSTOP);
		getpid();
	}
	else {
		sprintf(proc, "/proc/%i/mem", pid);
		if ((pfd = open(proc, O_RDWR)) < 0) {
			perror("open");
			return 1;
		}

		waitpid(pid, &status, 0);
		assert(WIFSTOPPED(status));
		assert(WSTOPSIG(status) == SIGSTOP);

		ptrace(PT_TO_SCE, pid, (caddr_t)1, 0);
		waitpid(pid, &status, 0);
		assert(WIFSTOPPED(status));
		assert(WSTOPSIG(status) == SIGTRAP);

		if (ioctl(pfd, PIOCSTATUS, &ps) < 0) {
			perror("ioctl");
			return 1;
		}

		fprintf(stderr, "ps.why = %d\n", ps.why);
		close(pfd);
		return 0;
	}
}
