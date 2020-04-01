"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"
"""

import os


class Create:
    def __init__(self, name, location):
        self.directory_name = name
        self.location = location
        self.directory_pwd = None

    @property
    def create_directory(self):
        self.directory_pwd = os.path.join(self.location, self.directory_name)
        try:
            if not os.path.exists(self.directory_pwd):

                os.mkdir(self.directory_pwd)
                if os.path.isdir(self.directory_pwd):
                    return 1

        except FileExistsError:
            return -1, "directory exists at path"
        return -1

    def create_file(self, name, extension, data):
        try:
            file_name = "{}.{}".format(name, extension)
            file = os.path.join(self.directory_pwd, file_name)
            if os.path.exists(file):
                print("file exist, overriding")

            with open(file, 'w+') as f:
                f.write(data)
        except:
            return -1
        return 1
