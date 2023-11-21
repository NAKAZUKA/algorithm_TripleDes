def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_binary_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data.tobytes())


def write_text_file(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)
