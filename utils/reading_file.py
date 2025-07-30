def read_file(file_path: str):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'Could not find file: {file_path}')
