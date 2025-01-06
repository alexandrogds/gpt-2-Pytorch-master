"""
This module is used to decompress the compressed data.
"""
import struct
from tqdm import tqdm

def decompress_data(input_file):
    # Read dictionary
    print("Reading dictionary...")
    replacements = {}
    
    with open(input_file + '.dict', 'rb') as f:
        # Read encoding flag
        is_encoded = struct.unpack('I', f.read(4))[0]
        encoding = None
        if is_encoded:
            enc_len = struct.unpack('I', f.read(4))[0]
            encoding = f.read(enc_len).decode('ascii')
        
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
        compressed_data = f.read()
    
    # Decompress data
    print("Decompressing data...")
    result = bytearray(compressed_data)  # Make a copy to work with
    
    # Sort tokens by length in descending order to handle overlapping sequences
    sorted_tokens = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
    
    with tqdm(total=len(sorted_tokens)) as pbar:
        for token, sequence in sorted_tokens:
            # Replace all occurrences of token with original sequence
            current_pos = 0
            while True:
                pos = result.find(token, current_pos)
                if pos == -1:
                    break
                result[pos:pos + len(token)] = sequence
                current_pos = pos + len(sequence)
            pbar.update(1)
    
    # Save decompressed data
    if encoding:
        try:
            # Decode the entire result as text
            decoded_text = result.decode(encoding)
            with open(input_file + '.decompressed', 'w', encoding=encoding) as f:
                f.write(decoded_text)
        except UnicodeDecodeError as e:
            print(f"Warning: Could not decode as {encoding}, saving as binary")
            with open(input_file + '.decompressed', 'wb') as f:
                f.write(result)
    else:
        with open(input_file + '.decompressed', 'wb') as f:
            f.write(result)
    
    print(f"Decompressed size: {len(result):,} bytes")

if __name__ == "__main__":
    input_file = "LICENSE"
    decompress_data(input_file)
