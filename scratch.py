
import os
import sys

def main(path):
    fwords = []
    for root, dirs, files in os.walk(path):

        for filenames in files:
            fname = filenames.split('-')
            if fname:
                fwords.append(fname[0])
        fword = list(set(fwords))
        print(fword)

    if __name__ == "__main__":
        path = sys.argv[1]
        print(f"Working on Path: {path}")