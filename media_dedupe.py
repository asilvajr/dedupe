#!/usr/bin/python3

import csv
import hashlib
import math
import os
import re
import send2trash
import platform
import sys
import argparse

defaults = {}

video_type = "video"
video_accepted_types = ['ts','mp4','flv','avc','wmv','av1','h.265','mpg','mpeg']

photo_type = "photo"
photo_accepted_types = ['jpg','png','gif','tiff','raw']


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


def get_default_directory():
    return defaults["directory"]


def process_args(parser):
    parser.add_argument("-f", "--source-file", help="File listing pre-populated names and hashes.")
    parser.add_argument("directory", help="Directory intended to be scanned")

    return parser.parse_args()


def review_ingest_history():
    with open("dedupe_records.txt","r+") as drf:
        for line in drf.readlines():
            # filename , sha256, 
            record_info = line.split(',')



def main(argv):
    args = process_args(argparse.ArgumentParser())

    cache = review_ingest_history()

    if args.directory:
        path = args.directory
    else:
        path = get_default_directory()
    print("Scanning path:", path)


    fht, dupe_table = scan_directory(path)

    print_table(dupe_table)


if __name__== "__main__":
    main(sys.argv)
