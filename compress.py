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
    
    # Calculate total iterations for progress bar
    total_iterations = data_len - MIN_SEQUENCE_LENGTH + 1
    
    # Add progress bar for sequence search
    with tqdm(total=total_iterations, desc="Finding sequences") as pbar:
        for i in range(data_len - MIN_SEQUENCE_LENGTH + 1):
            seq = data[i:i + MIN_SEQUENCE_LENGTH]
            sequences[seq].append(i)
            pbar.update(1)
    
    # Keep only sequences that appear more than once
    return {k: v for k, v in sequences.items() if len(v) > 1}

def compress_data(input_file, encode=None):
    # Read input file
    if encode:
        with open(input_file, 'r', encoding=encode) as f:
            text_data = f.read()
            data = text_data.encode(encode)
    else:
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
    
    # Save dictionary and compressed data with encoding info
    with open(input_file + '.dict', 'wb') as f:
        # Save encoding flag
        f.write(struct.pack('I', 1 if encode else 0))
        if encode:
            enc_bytes = encode.encode('ascii')
            f.write(struct.pack('I', len(enc_bytes)))
            f.write(enc_bytes)
        
        # Save dictionary size and entries
        f.write(struct.pack('I', len(replacements)))
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
    input_file = "LICENSE"
    encode = 'utf-8'  # Set to None for binary files
    compress_data(input_file, encode)
