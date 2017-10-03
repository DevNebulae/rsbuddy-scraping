from fsutils.touch import touch, touch_dir

def write_file(path, content):
    '''
    Write a string to a file and create the file if it does
    not exist.
    '''
    touch_dir(path)
    touch(path)

    with open(path, 'w+') as _file:
        _file.write(content)
