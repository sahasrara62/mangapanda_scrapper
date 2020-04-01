"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"
"""

import os
from os import walk


class Create:
    def __init__(self, name, location):
        self.base_dir = self.base_manga_directory(name, location)
        self.pro_dir = self.base_dir
    def create_directory(self, name, location):

        directory_pwd = os.path.join(location, name)
        try:
            if not os.path.isdir(directory_pwd):

                os.mkdir(directory_pwd)
                if os.path.isdir(directory_pwd):
                    return directory_pwd

        except FileExistsError:
            print('file exist')
        return directory_pwd

    def base_manga_directory(self, name, location):
        base_directory_pwd = os.path.join(location, name)
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
