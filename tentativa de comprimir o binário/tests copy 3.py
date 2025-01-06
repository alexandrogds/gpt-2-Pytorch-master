
"""
"""

import os; import sys; import struct
from collections import defaultdict
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor

CHUNK_SIZE = 512 * 1024 * 1024  # 512MB chunks
MIN_SEQUENCE_LENGTH = 1
MAX_SEQUENCE_LENGTH = 100

def find_sequences(data):
    sequences = defaultdict(list)
    data_len = len(data)

    # Calculate total iterations for progress bar
    total_iterations = data_len - MIN_SEQUENCE_LENGTH + 1
    # print(total_iterations)

    # with (total=100*total_iterations, desc="Finding sequences", mininterval=1) as pbar:
    def process_sequence(seq_length):
        aux = defaultdict(list)
        for i in range(data_len - seq_length + 1):
                seq = data[i:i + seq_length]
                sequences[seq].append(i)
                aux[seq].append(i)
        for k, v in aux.items():
            if len(v) == 0:
                print(k)
                exit()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_sequence, seq_length) for seq_length in tqdm(range(MIN_SEQUENCE_LENGTH, MAX_SEQUENCE_LENGTH + 1))]
        for future in futures: future.result()

                # print(sys.getsizeof(seq))
                # print(len(seq))
                # print(len(sequences[seq]))
                # print(len(str(i)))
                # exit()

    # Keep only sequences that appear more than once
    return {k: v for k, v in sequences.items() if len(v) > 1}
    # verificar nao tirar os que tem 1 e rodar so esse for e no descompress descomprimir

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
    MAX_TOKENS = 65024  # (254 * 256)
    
    for seq in sequences.keys():
        if token_value >= MAX_TOKENS:
            print("Warning: Maximum token limit reached. Some sequences will not be compressed.")
            break
            
        # Generate token bytes
        high_byte = (token_value // 256) % 256
        low_byte = token_value % 256
        token = bytes([high_byte, low_byte])
        
        replacements[seq] = token
        token_value += 1
    
    # Compress data by replacing sequences
    print("Compressing data...")
    compressed_data = bytearray(data)
    for seq, token in tqdm(replacements.items()):
    # for seq, positions in tqdm(sequences.items()):
        pos = 0
        while True:
            pos = data.find(seq, pos)
            if pos == -1:
                break
            compressed_data[pos:pos + len(seq)] = token

            # print(pos)
            # print(len(seq))
            # print(positions)
            # compressed_data[pos:pos + len(seq)] = positions

            # print(sys.getsizeof(token))
            # print(len(token))
            # with open('tests.bin', 'wb') as f:
            #     f.write(token)
            # with open('tests.bin', 'rb') as f:
            #     print(sys.getsizeof(f.read()))
            # with open('tests.bin', 'rb') as f:
            #     print(len(f.read()))
            # exit()

            pos += 1
    
    # Save dictionary and compressed data
    with open(input_file + '.dict', 'wb') as f:
        # Save dictionary size
        f.write(struct.pack('I', len(replacements)))
        # Save each sequence and its token
        for seq, token in replacements.items():
            print('===================OK====================')
            f.write(struct.pack('I', len(seq)))
            print(struct.pack('I', len(seq)))
            print(len(seq))
            f.write(seq)
            f.write(token)
            exit()

            print(sys.getsizeof(token))
            # with open('tests.bin', 'wb') as f:
            #     f.write(token)
            # with open('tests.bin', 'rb') as f:
            #     print(sys.getsizeof(f.read()))
            # exit()
    
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
    input_file = r"C:\Users\user\Downloads\tqdm-4.67.1.tar.gz"
    compress_data(input_file)
