
"""
This script finds all sequences of bytes of a given length that appear more than once in a file.
"""

import os
from tqdm import tqdm
import gc

# Adjust chunk size to stay within 4GB limit
CHUNK_SIZE = 512 * 1024 * 1024  # 512MB chunks
MAX_SEQUENCES_PER_CHUNK = 1000000

def find_sequences_in_chunk(chunk, min_len=2, max_len=2):
    chunk_size = len(chunk)
    seen_sequences = {}
    
    # Process only sequences of length 2 to save memory
    seq_len = 2
    
    for i in range(chunk_size - seq_len + 1):
        sequence = chunk[i:i + seq_len]
        if len(seen_sequences) >= MAX_SEQUENCES_PER_CHUNK:
            # Write current sequences and clear memory
            yield from ((seq, pos) for seq, pos in seen_sequences.items() if len(pos) > 1)
            seen_sequences.clear()
            gc.collect()
            
        if sequence in seen_sequences:
            seen_sequences[sequence].append(i)
        else:
            seen_sequences[sequence] = [i]
    
    # Yield remaining sequences
    yield from ((seq, pos) for seq, pos in seen_sequences.items() if len(pos) > 1)

def process_file(file_path):
    # Open output file early to write results incrementally
    with open(file_path + '.sequences', 'w') as out_f:
        with open(file_path, 'rb') as f:
            # Get file size for progress bar
            f.seek(0, 2)
            file_size = f.tell()
            f.seek(0)
            
            # Process file in chunks
            with tqdm(total=file_size, desc="Processing file") as pbar:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    
                    # Process each chunk
                    for sequence, positions in find_sequences_in_chunk(chunk):
                        # Write results immediately
                        out_f.write(f"Sequence (hex): {sequence.hex()}\n")
                        out_f.write(f"Length: {len(sequence)} bytes\n")
                        out_f.write(f"Positions: {positions}\n")
                        out_f.write("-" * 50 + "\n")
                        out_f.flush()  # Ensure writing to disk
                    
                    pbar.update(len(chunk))

def main():
    file_path = "gpt2-pytorch_model.bin"
    file_path = "LICENSE"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return
    
    process_file(file_path)
    print("Done! Results written to sequences_report.txt")

if __name__ == "__main__":
    main()
