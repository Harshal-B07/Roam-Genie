# helper function to read the prompt file

def read_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
