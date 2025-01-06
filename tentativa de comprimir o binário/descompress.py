"""
This module is used to decompress the compressed data.
"""
import struct
from tqdm import tqdm

def decompress_data(input_file, encode=None):
    # Read dictionary
    print("Reading dictionary...")
    replacements = {}
    with open(input_file + '.dict', 'rb') as f:
        # Read dictionary size
        dict_size = struct.unpack('I', f.read(4))[0]
        
        # Read each sequence and its token
        for _ in range(dict_size):
            seq_len = struct.unpack('I', f.read(4))[0]
            sequence = f.read(seq_len)
            token = f.read(2)
            replacements[token] = sequence
    
    # Read compressed data
    print("Reading compressed data...")
    with open(input_file + '.compressed', 'rb') as f:
        data = f.read()
    
    # Decompress data by replacing tokens with original sequences
    print("Decompressing data...")
    decompressed_data = bytearray(data)
    for token, sequence in tqdm(replacements.items()):
        pos = 0
        while True:
            pos = data.find(token, pos)
            if pos == -1:
                break
            decompressed_data[pos:pos + len(token)] = sequence
            pos += 1
    
    if encode:
        # Save decompressed data
        with open(input_file + '.decompressed', 'w', encoding=encode) as f:
            f.write(decompressed_data.decode(encode))
    else:
        with open(input_file + '.decompressed', 'wb') as f:
            f.write(decompressed_data)
    
    print(f"Decompressed size: {len(decompressed_data):,} bytes")

if __name__ == "__main__":
    input_file = "gpt2-pytorch_model.bin"
    input_file = "LICENSE"
    encode = 'utf-8'
    decompress_data(input_file, encode)
