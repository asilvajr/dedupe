#!/usr/bin/python3

# Build a Hashtable using a python dict. 
# Dict(Key => Value) => Dict(Sha256-Hash => List[(Filenames, Size,Date, Quality)])
# Output to file the results

import csv
import hashlib
import math
import os
import re
import send2trash
import platform
import sys
import argparse


BUF_SIZE = 1048576*256

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
    dupe_count = 0
    file_hash_table = {}
    for root, dirs, files in os.walk(path, topdown=True):
        list_size = len(files)
        for i, filename in enumerate(files):
            file_hash = get_file_hash(os.path.join(root,filename))
            if file_hash not in file_hash_table:
                file_hash_table[file_hash] = [os.path.join(root,filename)]
            else:
                file_hash_table[file_hash].append(os.path.join(root,filename))
                dupe_count = dupe_count + 1

            if i % 10 == 0:
                print(f"Processed {i} out of {list_size}. So far Dupe Count is {dupe_count}. ")

    # Dupes
    dupe_table = {}
    for k, v in file_hash_table.items():
        if len(v) > 1:
            dupe_table[k] = v
    print(f"So far, {len(dupe_table)} have been found...\n")
    return file_hash_table, dupe_table


def print_table(dupe_table):
    print(f"Table Size: {len(dupe_table)}")
    file_data_count = 0
    delete_file_count = 0
    rstr = r"\[[a-zA-Z ]*\]\s?[a-zA-Z0-9&\- ]*-\s?[a-zA-Z\0-9_', ]*"

    for k, v in dupe_table.items():
        for i in v:
            if re.search(rstr,i):
                v.insert(0, v.pop(v.index(i)))
        dupe_table[k] = v

    with open('dupe_record.txt','w') as dupe_record:
        for k, v in dupe_table.items():
            skipped = False
            dupe_record.write(f"{k} => {v}\n\n")
            for idx, i in enumerate(v):
                rstr = r"\[[a-zA-Z ]*\]\s?[a-zA-Z0-9&\- ]*-\s?[a-zA-Z\0-9_', ]*"

                if idx == len(v)-1 or skipped:
                    dupe_record.write(f"Deleting file: {i}\n")
                    file_data_count = file_data_count + os.path.getsize(i)
                    delete_file_count = delete_file_count + 1
                    send2trash.send2trash(i)

                if re.search(rstr, i) and not skipped:
                    dupe_record.write(f"Matched {i}\n")
                    skipped = True
                    continue

        dupe_record.write(f"Deleting {delete_file_count} files or {convert_size(file_data_count)} of Data.")

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def verify_delete(to_be_deleted):
    return [fi for fi in to_be_deleted if fi[1].endswith('.mp4') and mimetypes.guess_type(fi[0])[0] in MP4_MIMETYPE]


def delete_files(to_be_deleted):
    print("Deleting Files...")
    to_be_deleted = verify_delete(to_be_deleted)
    freed_space = 0
    with (open('deleted.log','w') as del_file):
        del_file.write("Deleting " + str(len(to_be_deleted)) + " files.")
        for tbd_file in to_be_deleted:
            try:
                del_file.write(f"{tbd_file[0]}\n")
                freed_space = freed_space + os.path.getsize(tbd_file[0])
                send2trash.send2trash(tbd_file[0])
            except Exception as e:
                print("The Error is: ", e)
                del_file.write("The Error is: " + str(e) + "\n")
                del_file.write(str(traceback.print_exc()))
                break

        freed_up_disk_space = convert_size(freed_space)
        del_file.write("Freed Up space: %s \n" % freed_up_disk_space)
        del_file.write("Fin!\n")
        print("Freed Up space: %s \n" % freed_up_disk_space)
        print("Fin!")


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--source-file", help = "File listing pre-populated names and hashes.")
    parser.add_argument("directory",help="Directory intended to be scanned")
    args = parser.parse_args()

    path = args.directory
    print("Scanning path:", path)
    fht, dupe_table = scan_directory(path)

    print_table(dupe_table)
    

if __name__=="__main__": 
    main(sys.argv) 
