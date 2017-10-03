import os

def touch(path):
    '''
    Create an empty file at the specified location.
    '''
    with open(path, 'a'):
        os.utime(path, None)

def touch_dir(path):
    '''
    Create a folder, including all of its subdirectories at
    the specified file path.
    '''
    base_directory = os.path.dirname(path)

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
