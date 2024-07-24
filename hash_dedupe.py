#!/usr/bin/python3

# Build a Hashtable using a python dict. 
# Dict(Key => Value) => Dict(Sha256-Hash => List[(Filenames, Size,Date, Quality)])
# Output to file the results


import hashlib
import os
import sys

from PIL import Image

BUF_SIZE = 1048576*16

def get_file_hash(filename):
    sha256 = hashlib.sha256()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()
    

def scan_directory(path):
    file_hash_table = {}
    for root, dirs, files in os.walk(path, topdown=True):
        list_size = len(files)
        for i, filename in enumerate(files):
            file_hash = get_file_hash(os.path.join(root,filename))
            if file_hash not in file_hash_table:
                file_hash_table[file_hash] = [os.path.join(root,filename)]
            else:
                file_hash_table[file_hash].append(os.path.join(root,filename))
            if i % 10 == 0:
                print("Proccessed", i, "out of", list_size)

    # Dupes
    dupe_table = {}
    for k, v in file_hash_table.items():
        if len(v) > 1:
            dupe_table[k] = v

    return file_hash_table, dupe_table


def print_table(dupe_table):
    for k,v in dupe_table.items():
        for i in v:
            print(k, "=>", v)

def main(argv):
    path = argv[1]
    print("Scanning path:", path)
    fht, dupe_table = scan_directory(path)

    print_table(dupe_table)
    

if __name__=="__main__": 
    main(sys.argv) 