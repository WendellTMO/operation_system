#include <sys/wait.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int count() {
	return 100;
}

int main(int argc, char** argv) {
	int fd[2], nbytes, sum;
	char estado = 'p';
	int my_pid = getpid();
    	int child_pid;
	pipe(fd);

    	printf("%d: processos antes da criação do processo filho\n", my_pid);
	if ((child_pid = fork()) == 0) {
		/* close input */
		close(fd[0]);
        	my_pid = getpid();
        	printf("%d: o valor da variável estado no processo filho é: %c\n", my_pid, estado);
       		
		write(fd[1], count(), 10);
		exit(0);

	} else {
        	printf("%d: processos depois da criação do processo filho\n", my_pid);	
        	printf("%d: pai está esperando pelo filho: %d\n", my_pid, child_pid);
		/*closes output */
		close(fd[1]);
		wait(&child_pid);
		nbytes = read(fd[0], sum, sizeof(sum));
			
	}

    	return(0);
}
