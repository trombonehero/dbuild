#include <stdio.h>

#include <math.h>

void bar(void);

int main(int argc, char *argv[])
{
	printf("tan(1): %f\n", tan(1));

	bar();
	return 0;
}

