'''
General purpose utility module which is useful for working
with the file system.
'''

import json
import os

def read_json(path):
    with open(path) as _file:
        return json.load(_file)

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

def write_file(path, content):
    '''
    Write a string to a file and create the file if it does
    not exist.
    '''
    touch_dir(path)
    touch(path)

    with open(path, 'w+') as _file:
        _file.write(content)
