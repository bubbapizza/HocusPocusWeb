import os


def get_file_contents(path):
    if os.path.exists(path):
        with open(path, 'r') as pid:
            contents = pid.read()
            return contents
    return None
