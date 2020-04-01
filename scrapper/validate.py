"""
validate the file and link
"""

import os
import validators


class Validate:
    def __init__(self):
        pass

    def paths(self, *paths):
        """
        check if path exists or not
        :param paths: list of path with the absolute address
        :return: return True if all path exists else throw error
        """
        result = [os.path.exists(path) for path in paths]

        return "path exists: {} \n path doesn't exist: {}".format(result.count(1), result.count(0))

    def files(self, files):
        result = [os.path.isfile(file) for file in files]
        return "file exists: {}\n file not exists: {}".format(result.count(1), result.count(0))

    def links(self, urls):
        """
        validate list of urls
        :param urls: list of valid url, url must include http:// or https://
        :return: string

        """
        result = [True if validators.url(url, public=True) else False for url in urls]
        return "valid url: {}\n Non valid url: {}".format(result.count(1), result.count(0))
