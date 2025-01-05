"""
This module is used to compress the data of gpt2-pytorch_model.bin file.
"""

import os
from collections import defaultdict
from tqdm import tqdm

def find_sequences(data, min_len=2):
    file_size = len(data)
    max_len = file_size // 2
    max_len = 2
    sequences = defaultdict(list)
    
    # Calculate total iterations for progress bar
    total_iterations = sum(file_size - seq_len + 1 for seq_len in range(min_len, max_len + 1))
    
    with tqdm(total=total_iterations, desc="Searching sequences") as pbar:
        for seq_len in range(min_len, max_len + 1):
            for i in range(file_size - seq_len + 1):
                sequence = data[i:i + seq_len]
                sequences[sequence].append(i)
                pbar.update(1)
            
            # Keep only sequences that appear more than once
            sequences = {k: v for k, v in sequences.items() if len(v) > 1}
    
    # # Remove sequences that are subsequences of other sequences
    # filtered_sequences = {}
    # for seq, positions in sequences.items():
    #     if not any(seq in other_seq and seq != other_seq for other_seq in sequences):
    #         filtered_sequences[seq] = positions
    
    # return filtered_sequences
    return sequences

def main():
    file_path = "gpt2-pytorch_model.bin"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return
    
    # Read binary file
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Find repeating sequences
    sequences = find_sequences(data)
    
    # Save results
    with open('sequences_report.txt', 'w') as f:
        for sequence, positions in sequences.items():
            f.write(f"Sequence (hex): {sequence.hex()}\n")
            f.write(f"Length: {len(sequence)} bytes\n")
            f.write(f"Positions: {positions}\n")
            f.write("-" * 50 + "\n")

if __name__ == "__main__":
    main()
