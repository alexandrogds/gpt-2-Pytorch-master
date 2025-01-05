"""
This module is used to compress the data.
"""
import os
import struct
from collections import defaultdict
from tqdm import tqdm

CHUNK_SIZE = 512 * 1024 * 1024  # 512MB chunks
MIN_SEQUENCE_LENGTH = 2
MAX_SEQUENCE_LENGTH = 2

def find_sequences(data):
    sequences = defaultdict(list)
    data_len = len(data)
    
    for i in range(data_len - MIN_SEQUENCE_LENGTH + 1):
        seq = data[i:i + MIN_SEQUENCE_LENGTH]
        sequences[seq].append(i)
    
    # Keep only sequences that appear more than once
    return {k: v for k, v in sequences.items() if len(v) > 1}

def compress_data(input_file):
    # Read input file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Find repeating sequences
    print("Finding sequences...")
    sequences = find_sequences(data)
    
    # Create replacement dictionary
    replacements = {}
    current_token = b'\xFF\x00'  # Start with a unique token
    
    for seq in sequences.keys():
        token = current_token
        replacements[seq] = token
        # Generate next token
        current_token = bytes([current_token[0], current_token[1] + 1])
    
    # Compress data by replacing sequences
    print("Compressing data...")
    compressed_data = bytearray(data)
    for seq, token in tqdm(replacements.items()):
        pos = 0
        while True:
            pos = data.find(seq, pos)
            if pos == -1:
                break
            compressed_data[pos:pos + len(seq)] = token
            pos += 1
    
    # Save dictionary and compressed data
    with open(input_file + '.dict', 'wb') as f:
        # Save dictionary size
        f.write(struct.pack('I', len(replacements)))
        # Save each sequence and its token
        for seq, token in replacements.items():
            f.write(struct.pack('I', len(seq)))
            f.write(seq)
            f.write(token)
    
    # Save compressed data
    with open(input_file + '.compressed', 'wb') as f:
        f.write(compressed_data)
    
    original_size = len(data)
    compressed_size = len(compressed_data)
    print(f"Compression ratio: {compressed_size/original_size:.2%}")
    print(f"Original size: {original_size:,} bytes")
    print(f"Compressed size: {compressed_size:,} bytes")

if __name__ == "__main__":
    input_file = "gpt2-pytorch_model.bin"
    file_path = "LICENSE"
    compress_data(input_file)
