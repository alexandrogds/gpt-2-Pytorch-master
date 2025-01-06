"""testar se o compress.py esta certo
"""
from tqdm import tqdm
import struct; import sys

def testar(input_file):
    c = None
    with open(input_file, 'rb') as f:
        c = f.read()
    s = {}
    for i in tqdm(range(0, len(c)-1), desc="Analyzing pairs", mininterval=1.0):
        # Combine two bytes into a single 16-bit value
        two_byte_value = struct.unpack('>H', bytes([c[i], c[i+1]]))[0]
        s[two_byte_value] = s.get(two_byte_value, 0) + 1
    all_ones = all(count == 1 for count in s.values())
    if all_ones:
        print(f"Todos os pares ocorrem exatamente uma vez.")
    else:
        print(f"Alguns pares ocorrem mais de uma vez.")

if __name__ == "__main__":
    # input_file = "gpt2-pytorch_model.bin"
    input_file = r"C:\Users\user\Downloads\rufus-4.6p.exe"
    testar(input_file)