#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
	if(argc <= 1) {
		printf("No file name provided\n");
		return 1;
	}

	if(strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
		printf("Command line interface that converts .flp <-> .rte files \n\nUsage:\n\n   main [-h | --help] <Filename>\n\n   -h | --help:  Prints this help text\n");
		return EXIT_SUCCESS;
	}
	printf("%s\n", argv[1]);
	return EXIT_SUCCESS;
}
