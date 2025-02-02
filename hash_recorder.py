#!/usr/bin/python3

import csv
import hashlib
import logging
import math
import os
import re
import platform
import sys
import argparse
import mimetypes


BUF_SIZE = 1048576*256
defaults = {}


accepted_file_types = ['video/mp2t', 'video/mp4']

def process_args(parser):
    parser.add_argument("-f", "--source-file", help="File listing pre-populated names and hashes.")
    parser.add_argument("directory", help="Directory intended to be scanned")

    return parser.parse_args()


def review_ingest_history(path):

    file_path = os.path.join(path,"hash_records.txt")
    print(f"Hash Records: {file_path}")
    if not os.path.exists(file_path):
        with open(file_path,"w") as f:
            f.write("")
        return {}
    else:
        with open(file_path,"r+") as drf:
            return {line.split(',')[0]: line.split(',')[1] for line in drf.readlines()}


def get_file_hash(filename):
    sha256 = hashlib.sha256()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def get_list_of_videos(root, files):
    return [f for f in files if mimetypes.guess_type(os.path.join(root,f))[0] in accepted_file_types]
    #l = []
    #for f in files:
    #    #print(f" {f} mimetype {typo}")
    #    if mimetypes.guess_type(os.path.join(root,f))[0] in accepted_file_types:
    #        l.append(f)
    #return l

def scan_directory(path, cache={}):
    dupe_count = 0
    file_hash_table = {}

    for root, dirs, files in os.walk(path, topdown=True):
        print(f"Files: {len(files)}")
        vid_files = get_list_of_videos(root, files)
        list_size = len(vid_files)
        print(f"Reduces Files: {len(vid_files)}")
        # Reduce files List

        with open(os.path.join(root,"hash_records.txt"), "a+") as hr:
            for i, filename in enumerate(vid_files):
                file_hash = get_file_hash(os.path.join(root,filename))
                if file_hash not in cache:
                    hr.write(file_hash + "," + filename + "\n")

                if list_size > 100 and \
                        i % 10 == 0:
                    print(f"Processed {i} out of {list_size}. So far Dupe Count is {dupe_count}. ")

    # Dupes
    dupe_table = {}
    for k, v in file_hash_table.items():
        if len(v) > 1:
            dupe_table[k] = v
    print(f"So far, {len(dupe_table)} have been found...\n")
    return file_hash_table, dupe_table


def get_default_directory():
    return defaults["directory"]


def main(argv):
    args = process_args(argparse.ArgumentParser())

    if args.directory:
        path = args.directory
    else:
        path = get_default_directory()

    cache = review_ingest_history(path)
    print("Scanning path:", path)
    scan_directory(path, cache)



def set_defaults():
    os_detected = platform.system()

    # Mac Book
    if os_detected == 'Darwin':
        defaults["directory"] = "/Users/asilvajr/Downloads"
    elif os_detected == "Windows":
        defaults["directory"] = " "
    elif os_detected == "Linux":
        defaults["directory"] = " "
    else:
        defaults["directory"] = None


if __name__== "__main__":
    set_defaults()
    main(sys.argv)
