"""testar se o compress.py esta certo
"""
from tqdm import tqdm

def testar(input_file):
    c = None
    with open(input_file, 'rb') as f:
        c = f.read()
    s = {}
    for i in tqdm(range(0, len(c)-1), desc="Analyzing pairs", mininterval=1.0):
        pair = (c[i], c[i+1])
        s[pair] = s.get(pair, 0) + 1
    all_ones = all(count == 1 for count in s.values())
    print(f"All pairs occur exactly once.")

if __name__ == "__main__":
    input_file = "gpt2-pytorch_model.bin"
    # input_file = r"C:\Users\user\Downloads\rufus-4.6p.exe"
    testar(input_file)