# create_tempfile.py

import os, atexit
from random import randint

def create_tempfile():
    pid = os.getpid()
    while True:
        random_digits = ''.join(chr(ord('0')+randint(0,9)) for x in range(16))
        path = '/tmp/{}-{}.tmp'.format(pid, random_digits)
        if not os.path.exists(path): break
    f = open(path, "w+")
    def cleanup():
        print "Closing and removing temp file: {}".format(path)
        f.close()
        if os.path.exists(path):
            os.unlink(path)
    atexit.register(cleanup)
    return f

