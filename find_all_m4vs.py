"""
Find all files with .m4v extention in specified directory trees.
Then compare same name file's lengths
"""
import os
from os.path import join, getsize
import argparse
import pprint

all_files = {}

def process_cmdline():
    """
    Process command line arguments and return them
    """
    parser = argparse.ArgumentParser(description='Find m4v files.')
    parser.add_argument('--dir', action='append', help="Add directory to trees to be scanned")
    args = parser.parse_args()
    return args

def find_all_m4vs_in_dir(dir):
    """
    Check all files in a directory tree and save information about .m4v files
    """
    for root, _, files in os.walk(dir):
        for filename in files:
            if not filename.endswith('.m4v'): 
                continue

            size = getsize(join(root,filename))

            file_info = {
                'dir': root,
                'size': size,
            }
            try:
                all_files[filename].append(file_info)
            except KeyError as e:
                all_files[filename] = [file_info]

def do_file_sizes_match(f):
    sizes = set([a['size'] for a in all_files[f]])
    return len(sizes) == 1

def find_duplicates():
    for f in all_files:
        if len(all_files[f]) > 1:
            if not do_file_sizes_match(f):
                print("File-->%s"%f)
                pprint.pprint(all_files[f],indent=10)

if __name__ == "__main__":
    args= process_cmdline()
    print(args)
    if args.dir:
        for dir in args.dir:
            find_all_m4vs_in_dir(dir)
    find_duplicates()

    # pprint.pprint(all_files, width=150)