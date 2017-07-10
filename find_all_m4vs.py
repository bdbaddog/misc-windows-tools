"""
Find all files with .m4v extention in specified directory trees.
Then compare same name file's lengths
"""
import os
from os.path import join, getsize
import argparse
import pprint

SF_FILES = {}
PLEX_FILES = {}
ALL_FILES = {}

def process_cmdline():
    """
    Process command line arguments and return them
    """
    parser = argparse.ArgumentParser(description='Find m4v files.')
    parser.add_argument('--dir', action='append', help="Add directory to trees to be scanned")
    parser.add_argument('--plex', action='append', help="Root dir for plex files")
    args = parser.parse_args()
    return args

def find_all_m4vs_in_dir(dir, files_dict):
    """
    Check all files in a directory tree and save information about .m4v files
    """
    for root, _, files in os.walk(dir):
        for filename in files:
            if not filename.endswith('.m4v'): 
                continue

            size = getsize(join(root, filename))

            file_info = {
                'dir': root,
                'size': size,
            }
            try:
                files_dict[filename].append(file_info)
            except KeyError as e:
                files_dict[filename] = [file_info]

def do_file_sizes_match(f):
    sizes = set([a['size'] for a in all_files[f]])
    return len(sizes) == 1

def find_duplicates(files_dict):
    for f in files_dict:
        if len(files_dict[f]) > 1:
            if not do_file_sizes_match(f):
                print("File-->%s"%f)
                pprint.pprint(files_dict[f], indent=10)

def print_report(sf_movies, nyc_movies):
    not_in_nyc = sf_movies - nyc_movies
    not_in_sf  = nyc_movies - sf_movies
    all_movies = sf_movies and nyc_movies

    max_len = max([len(f) for f in all_movies])

    print("=======Only in SF=========")
    for f in sorted(not_in_nyc):
        print('Movie:{0: >{width}}  Location:{1}'.format(f, [x['dir'] for x in ALL_FILES[f]], width=max_len,))

    print("=======Only in NY=========")
    for f in sorted(not_in_sf):
        try:
            print('Movie:{0: >{width}}  Location:{1}'.format(f, [x['dir'] for x in ALL_FILES[f]], width=max_len,))
        except KeyError as e:
            import pdb; pdb.set_trace()

    # for f in sorted(all_movies):
    #     print('Movie:{0: >{width}} SF:{1:6}  Plex:{2:6}'.format(f,(f in sf_movies),(f in nyc_movies), width=max_len,))



if __name__ == "__main__":
    args= process_cmdline()
    print(args)
    if args.dir:
        for dir in args.dir:
            find_all_m4vs_in_dir(dir, SF_FILES)
    if args.plex:
        for dir in args.plex:
            find_all_m4vs_in_dir(dir, PLEX_FILES)

    sf_movies = set(SF_FILES.keys())
    nyc_movies = set(PLEX_FILES.keys())

    ALL_FILES = SF_FILES.copy()
    for f in PLEX_FILES:
        if f in ALL_FILES:
            ALL_FILES[f].extend(PLEX_FILES[f])
        else:
            ALL_FILES[f] = PLEX_FILES[f]


    print_report(sf_movies, nyc_movies)

    # find_duplicates()

    # pprint.pprint(ALL_FILES, width=150)