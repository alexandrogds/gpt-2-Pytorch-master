#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNK_SIZE (512 * 1024 * 1024)  // 512MB chunks
#define MAX_POSITIONS (1024 * 1024 * 256)  // Limit positions array
#define MAX_SEQUENCES 1000000

// Structure to store a sequence and its positions
typedef struct {
    unsigned char* sequence;
    size_t length;
    size_t* positions;
    size_t pos_count;
} Sequence;

// Structure to store all sequences
typedef struct {
    Sequence* sequences;
    size_t count;
} SequenceList;

// Initialize a new sequence list
SequenceList* create_sequence_list() {
    SequenceList* list = (SequenceList*)malloc(sizeof(SequenceList));
    list->sequences = (Sequence*)malloc(MAX_SEQUENCES * sizeof(Sequence));
    list->count = 0;
    return list;
}

// Add a sequence if it appears more than once
void add_sequence(SequenceList* list, unsigned char* data, size_t seq_len, size_t file_size) {
    size_t* positions = (size_t*)malloc(MAX_POSITIONS * sizeof(size_t));
    size_t pos_count = 0;

    // Find all positions of the sequence
    for (size_t i = 0; i <= file_size - seq_len; i++) {
        int match = 1;
        for (size_t j = 0; j < seq_len; j++) {
            if (data[i + j] != data[i + j]) {
                match = 0;
                break;
            }
        }
        if (match) {
            positions[pos_count++] = i;
        }
    }

    // If sequence appears more than once, add it to the list
    if (pos_count > 1) {
        list->sequences[list->count].sequence = (unsigned char*)malloc(seq_len);
        memcpy(list->sequences[list->count].sequence, data, seq_len);
        list->sequences[list->count].length = seq_len;
        list->sequences[list->count].positions = positions;
        list->sequences[list->count].pos_count = pos_count;
        list->count++;
    } else {
        free(positions);
    }
}

// Write results to file
void write_results(SequenceList* list, const char* output_file) {
    FILE* f = fopen(output_file, "w");
    if (!f) {
        printf("Error opening output file\n");
        return;
    }

    for (size_t i = 0; i < list->count; i++) {
        fprintf(f, "Sequence (hex): ");
        for (size_t j = 0; j < list->sequences[i].length; j++) {
            fprintf(f, "%02x", list->sequences[i].sequence[j]);
        }
        fprintf(f, "\nLength: %zu bytes\n", list->sequences[i].length);
        
        fprintf(f, "Positions: ");
        for (size_t j = 0; j < list->sequences[i].pos_count; j++) {
            fprintf(f, "%zu ", list->sequences[i].positions[j]);
        }
        fprintf(f, "\n%.*s\n", 50, "------------------------------------------------");
    }

    fclose(f);
}

// Free memory
void free_sequence_list(SequenceList* list) {
    for (size_t i = 0; i < list->count; i++) {
        free(list->sequences[i].sequence);
        free(list->sequences[i].positions);
    }
    free(list->sequences);
    free(list);
}

void process_file_in_chunks(const char* file_path) {
    FILE* f = fopen(file_path, "rb");
    if (!f) {
        printf("Error: %s not found\n", file_path);
        return;
    }

    // Get file size
    fseek(f, 0, SEEK_END);
    size_t file_size = ftell(f);
    fseek(f, 0, SEEK_SET);

    // Allocate chunk buffer
    unsigned char* chunk = (unsigned char*)malloc(CHUNK_SIZE);
    FILE* out_f = fopen("sequences_report.txt", "w");

    size_t bytes_read = 0;
    printf("Processing file in chunks...\n");

    while (bytes_read < file_size) {
        size_t current_chunk = fread(chunk, 1, CHUNK_SIZE, f);
        if (current_chunk == 0) break;

        // Process chunk
        SequenceList* sequences = create_sequence_list();
        add_sequence(sequences, chunk, 2, current_chunk);  // Fixed sequence length of 2
        
        // Write results for this chunk
        write_results(sequences, "sequences_report.txt");
        
        // Cleanup chunk data
        free_sequence_list(sequences);
        
        bytes_read += current_chunk;
        printf("Processed: %.2f%%\n", (float)bytes_read * 100 / file_size);
    }

    // Cleanup
    free(chunk);
    fclose(f);
    fclose(out_f);
}

int main() {
    process_file_in_chunks("gpt2-pytorch_model.bin");
    printf("Done! Results written to sequences_report.txt\n");
    return 0;
}
