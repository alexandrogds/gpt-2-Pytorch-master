"""
This is file to see if I can view the init of a file bin.
"""

try:
    with open('sequences_report.txt', 'r', encoding='utf-8') as file:
        content = file.read(100)
        print("First 100 characters:")
        print(content)
except UnicodeDecodeError:
    print("Warning: File contains binary data that cannot be decoded as UTF-8")
except FileNotFoundError:
    print("Error: gpt2-pytorch_model.bin file not found")