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
	long arg;
	pid_t pid;
	char proc[32];
	struct procfs_status ps;

	if ((pid = fork()) < 0) {
		perror("fork");
		return 1;
	}
	else if (!pid) {
		kill(getpid(), SIGSTOP);
		getpid();
	}
	else {
		sprintf(proc, "/proc/%i/mem", pid);
		if ((pfd = open(proc, O_RDWR)) < 0) {
			perror("open");
			return 1;
		}

		if (ioctl(pfd, PIOCBIS, S_SCE) < 0) {
			perror("PIOCBIS");
			return 1;
		}

		if (ioctl(pfd, PIOCCONT, 1) < 0) {
			perror("PIOCCONT");
			return 1;
		}

		if (ioctl(pfd, PIOCWAIT, &ps) < 0) {
			perror("PIOCWAIT");
			return 1;
		}

		fprintf(stderr, "ps.why = %d\n", ps.why);

		close(pfd);
		return 0;
	}
}
