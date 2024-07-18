#include <stdio.h>
#include <pthread.h>

static volatile int sum = 0;

void *count(void *arg) {
	sum += 100;
	return NULL;
}

int main(int argc, char *argv[]) {

	pthread_t p1, p2;
	pthread_create(&p1, NULL, count, 0);
	pthread_create(&p2, NULL, count, 0);

	pthread_join(p1, NULL);
	pthread_join(p2, NULL);
	printf("soma: %d\n", sum);
	return 0;
}
