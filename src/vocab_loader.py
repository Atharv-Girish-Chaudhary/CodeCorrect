def load_vocabulary(file_path):
    """
    Load vocabulary from a text file, one word per line.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]