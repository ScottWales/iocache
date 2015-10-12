# Modified from http://stackoverflow.com/a/3431835/208625

import hashlib

def checksum(filename, blocksize = 65536):
    afile  = open(filename, 'rb')
    buf    = afile.read(blocksize)
    hasher = hashlib.sha256()
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
