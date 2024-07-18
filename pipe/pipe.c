#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int count(int x) {
	return x + 100;
}

int main(int argc, char** argv) {
    int input = atoi(argv[1]), num = 0, fd[2];
    pid_t children[input];
    pipe(fd);
    for (int i = 0; i < input; i++) {
        if((children[i] = fork()) == 0) {
            if (i != 0) {
                read(fd[0], &num, sizeof(num));
            }
            if (i == input -1) {
                close(fd[0]);
            }
            num = count(num);
            write(fd[1], &num, sizeof(num));
            exit(0);
        }
    }
    for (int i = 0; i < input; i++) {
        waitpid(children[i], NULL, 0);
    }
/*close output*/
	close(fd[1]);
	read(fd[0], &num, sizeof(num));
    printf("Sum: %d\n", num);
    return(0);
}
