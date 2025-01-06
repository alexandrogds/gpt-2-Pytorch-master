#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define HASH_SIZE 65536  // 2^16 for all possible two-byte combinations

typedef struct {
    uint32_t count;
    uint8_t exists;
} HashEntry;

void show_progress(size_t current, size_t total) {
    static time_t last_update = 0;
    time_t now = time(NULL);
    
    // Update only once per second
    if (now == last_update) return;
    
    float percentage = (float)current / total * 100;
    printf("\rAnalyzing pairs: %.1f%% ", percentage);
    fflush(stdout);
    last_update = now;
}

void test_compress(const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        printf("Error opening file\n");
        return;
    }

    // Get file size
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Read entire file
    unsigned char* data = (unsigned char*)malloc(file_size);
    if (!data) {
        printf("Memory allocation failed\n");
        fclose(file);
        return;
    }
    fread(data, file_size, 1, file);
    fclose(file);

    // Initialize hash table
    HashEntry* pairs = (HashEntry*)calloc(HASH_SIZE, sizeof(HashEntry));
    if (!pairs) {
        printf("Hash table allocation failed\n");
        free(data);
        return;
    }

    // Count pairs
    for (long i = 0; i < file_size - 1; i++) {
        uint16_t two_byte_value = (data[i] << 8) | data[i + 1];
        pairs[two_byte_value].exists = 1;
        pairs[two_byte_value].count++;
        
        show_progress(i, file_size - 1);
    }
    printf("\n");

    // Check if all pairs occur exactly once
    int all_ones = 1;
    for (int i = 0; i < HASH_SIZE; i++) {
        if (pairs[i].exists && pairs[i].count != 1) {
            all_ones = 0;
            break;
        }
    }

    // Print counts for all pairs
    printf("Pair counts: ");
    for (int i = 0; i < HASH_SIZE; i++) {
        if (pairs[i].exists) {
            printf("%u", pairs[i].count);
            if (i < HASH_SIZE - 1) printf(", ");
        }
    }
    printf("\n");

    printf("All pairs occur exactly once: %s\n", all_ones ? "true" : "false");

    free(pairs);
    free(data);
}

int main() {
    // const char* input_file = "C:\\Users\\user\\Pictures\\Screenshots\\Captura de Tela (28).png";
    const char* input_file = "C:\\Users\\user\\Downloads\\rufus-4.6p.exe";
    // const char* input_file = "C:\\Users\\user\\OneDrive\\Attachments\\arquivo caso natalia.pdf";
    // const char* input_file = "C:\\Users\\user\\OneDrive\\Attachments\\Biomechanicalcyclingv8english.xls";
    test_compress(input_file);
    return 0;
}
