"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"
"""

import os
from os import walk
from pathlib import Path, PureWindowsPath


import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace='_'):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]



class Create:
    def __init__(self, name, location):


        self.base_dir = self.base_manga_directory(name, location)
        self.pro_dir = self.base_dir
    def create_directory(self, name, location):

        name = clean_filename(name).strip()

        directory_pwd = os.path.join(location, name)
        if os.name == 'nt':
            print("this is a window system")
            directory_pwd = Path(directory_pwd)
            directory_pwd = PureWindowsPath(directory_pwd).as_posix()


        try:
            if not os.path.isdir(directory_pwd):
                os.mkdir(directory_pwd)
                if os.path.isdir(directory_pwd):
                    return directory_pwd

        except FileExistsError:
            print('file exist')
        return directory_pwd

    def base_manga_directory(self, name, location):


        name = clean_filename(name).strip()
        base_directory_pwd = os.path.join(location, name)
        if os.name == 'nt':
            _base_directory_pwd = Path(base_directory_pwd)
            base_directory_pwd = PureWindowsPath(_base_directory_pwd).as_posix()


        if not os.path.isdir(base_directory_pwd):
            os.mkdir(base_directory_pwd)
            print("base directory created {} ".format(base_directory_pwd))
        else:
            print("base directory exist {}".format(base_directory_pwd))
        return  base_directory_pwd

    def get_all_directories(self):
        folders = []
        for (dirpath, dirnames, filenames) in walk(self.base_dir):
            folders.extend(filenames)
            break
        return folders
