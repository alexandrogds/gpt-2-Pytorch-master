// -*- coding: utf-8 -*-
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>
#include <stdint.h>
#include <time.h>

#define HASH_SIZE 65536  // 2^16 for all possible two-byte combinations

int main(int argc, char *argv[]) {
	setlocale(LC_ALL, "pt_BR.UTF-8");

	char filename[256];
	if (argc < 2) {
		printf("Usage: %s <filename>\n", argv[0]);
		return 1;
	}
	strncpy(filename, argv[1], sizeof(filename) - 1);
	filename[sizeof(filename) - 1] = '\0';
	FILE* file = fopen(filename, "rb");
    if (!file) {
        printf("Error opening file\n");
        return 1;
    }

    // Get file size
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
	if (file_size > 4294967295UL) {
		printf("O tamanho do arquivo é maior que o sizeof de long.\n");
	} else {
		printf("O tamanho do arquivo é menor que o sizeof de long.\n");
	}
	fclose(file);
    return 0;
}
