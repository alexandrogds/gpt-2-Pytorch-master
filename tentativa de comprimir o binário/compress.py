"""
This module is used to compress the data.
"""
import os
import sys
import struct
from collections import defaultdict
from tqdm import tqdm

CHUNK_SIZE = 512 * 1024 * 1024  # 512MB chunks
MIN_SEQUENCE_LENGTH = 140  # Começando com 140
MAX_SEQUENCE_LENGTH = 300  # Defina um valor limite superior apropriado

def find_sequences(data):
    sequences = defaultdict(list)
    data_len = len(data)
    
    # Add progress bar for sequence search
    with tqdm(total=data_len, desc="Finding sequences") as pbar:
        for seq_length in range(MIN_SEQUENCE_LENGTH, MAX_SEQUENCE_LENGTH + 1):
            for i in range(data_len - seq_length + 1):
                seq = data[i:i + seq_length]
                sequences[seq].append(i)

                pbar.update(1)
    
    # Keep only sequences that appear more than once
    return sequences
    # return {k: v for k, v in sequences.items() if len(v) > 1}

def compress_data(input_file):
    # Read input file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Find repeating sequences
    print("Finding sequences...")
    sequences = find_sequences(data)
    
    # Create replacement dictionary
    replacements = {}
    token_value = 0
    
    # Maximum number of tokens possible with 2 bytes (excluding 0xFF which is reserved)
    # MAX_TOKENS = 65024  # (254 * 256)
    
    for seq in sequences.keys():
        # if token_value >= MAX_TOKENS:
        #     print("Warning: Maximum token limit reached. Some sequences will not be compressed.")
        #     break
            
        # Generate token bytes
        # high_byte = (token_value // 256) % 256
        # low_byte = token_value % 256
        # token = bytes([high_byte, low_byte])
        
        replacements[seq] = token
        token_value += 1
    
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
    input_file = r"C:\Users\user\Downloads\rufus-4.6p.exe"
    compress_data(input_file)
