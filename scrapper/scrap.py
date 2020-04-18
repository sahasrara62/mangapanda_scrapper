"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"
"""
import os
import sys

import requests
from lxml import html
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
import json
from pathlib import Path, PureWindowsPath
from .create import clean_filename
import multiprocessing

import multiprocessing.pool
import functools

def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


class Download:
    def __init__(self):
        pass

    def get_page_urls(self, chapter_url):
        """
        return the url of the pages present for that chapter


        :param chapter_url:url of the chapter eg : "https://www.mangapanda.com/one-piece/1"
        :return: list of urls of the pages for that chapter eg ["https://www.mangapanda.com/one-piece/1".
        "https://www.mangapanda.com/one-piece/1/2" ..]
        """
        print("downloading chapter {}".format(chapter_url.split('/')[-1]))
        page_content = requests.get(chapter_url).content
        extract_rule = r'//*/div[@id="selectpage"]/select[@id="pageMenu"]'
        tree = html.fromstring(page_content)
        data = tree.xpath(extract_rule)[0]
        chapter_manga_page_links = [urljoin(self.web_url, '{}'.format(i.attrib['value'])) for i in data]
        return chapter_manga_page_links

    def save_manga(self, location, page_image_url, name, extension='jpg'):
        """

        :param location:
        :param page_image_url:
        :param name:
        :param extension:
        :param tqdm:
        :return:
        """

        name = clean_filename(name).strip()
        print(name)
        file_name = os.path.join(location, name +'.{}'.format(extension))

        if os.name =='nt':
            # handling downloading for windows file system
            file_name = Path(file_name)
            file_name = PureWindowsPath(file_name).as_posix()

        chunk_size = 1024
        wait = True


        r = requests.get(page_image_url, stream=True, timeout=30)


        with open(file_name, 'wb') as f:
            pbar = tqdm(unit="B", total=int(r.headers['Content-Length']))
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update(len(chunk))
                    f.write(chunk)
        if os.path.isfile(file_name):
            return True
        return False
    def save_details(self, data, location, ):

        if os.name=='nt':
            # handling windows path
            location = Path(location)
            location = PureWindowsPath(location).as_posix().strip()

        with open(os.path.join(location, 'info.json'), 'w+') as f:
            f.write(json.dumps(data))
        print("save details at location {}".format(location))

    def dowload_manga(self, urls, location, extension='jpg'):

        """

        :param extension:
        :param urls: list of all page urls
        :param location: where the chapter need to be saved
        :return: None
        """
        data = {}

        for index, page_url in enumerate(urls):
            wait = True
            dic = {'page_name': '', 'image_source': ''}

            while wait:
                try:
                    res = requests.get(page_url).content
                    path = r'//*/img[@id="img"]'
                    tree = html.fromstring(res)
                    result = tree.xpath(path)
                    print("downloading page {}".format(page_url.split('/')[-1]))

                    dic['page_name'], dic['image_source'] = result[0].attrib['alt'], result[0].attrib['src']
                    print("downloading image {}".format(dic['image_source']))

                    x = self.save_manga(location, dic['image_source'], dic['page_name'], extension=extension)

                    if x:
                        wait = False
                except  :
                        wait = True
                        print("Timeout : Redownloading again")


            data.update({index+1:dic})
        self.save_details(data, location)
        return data

    def get_chapters_details(self, manga_web_url, manga_name):

        """

        :return:  chapter details from the manga main page in the mangapanda.oom
        """
        address = urljoin(manga_web_url, manga_name)
        response = requests.get(address).content
        tree = html.fromstring(response)
        path = r'//*/div[@id="chapterlist"]/table[@id="listing"]/tr/td/a'
        res = tree.xpath(path)
        dic = {'chapter_name': '', 'url': ''}
        result = {}
        for chapter_number, chapter_details in enumerate(res):
            dic['chapter_name'] = "{} {}".format(chapter_details.text, chapter_details.tail)
            dic['url'] = manga_web_url + chapter_details.attrib['href']
            # dic['name'] = chapter_details.tail
            result.update({chapter_number + 1: dic})
            dic = {'chapter_name': '', 'url': ''}
        # self._save_details( result, self.location)
        return result





class Scrap(Download):
    def __init__(self, url, chapter=None, start=None, end=None, location=None):
        """
        Base Scrap class which store the scrapping details


        :param url: manga page url example : https://www.mangapanda.com/one-piece
        :param chapter: chapter_url example : https://www.mangapanda.com/one-piece/1 # dont include extra / at end
        :param start: if a list of chapter to download
        :param end: end chapter which need to download
        :param location: location where manga chapter will be saved
        """

        super().__init__()
        self.manga_url = url
        self.chapter = chapter

        self.location = self._get_location(location)
        self.manga_name = urlparse(self.manga_url)[2].split('/')[1]
        self.web_url = urlparse(self.manga_url)[0] + '://' + urlparse(self.manga_url)[1]
        self.details = self.get_chapters_details(self.web_url, self.manga_name)
        self.start_chapter = 0
        self.end_chapter = 99999999
        self.set_chapter_start_end(chapter, start, end)

    def _get_location(self, location):


            if location is not None:
                if os.name =="nt":
                    location = Path(location)
                    location = PureWindowsPath(location).as_posix()

                return location
            return os.path.dirname(os.path.realpath(__file__))

    def _get_start(self, start):
        if start is not None:
            return int(start)
        if start is None:
            start = 1

        info =self.details
        new_start = -1
        if  isinstance(start, int) and start<=len(self.details) and start>=1:
            if start in info.keys():
                new_start = start
        else:
            print("invalid start chapter, starting form1")
            new_start = min(info.keys())
        return int(new_start)


    def _get_end(self, end):
        if end is not None:
            return int(end)
        if end is None:
            end = 9999999
        end_ = 0
        if isinstance(end, int) and end<=len(self.details.keys()) and end>=1:
            if end in self.details.keys():
                end_ = end
        else:
            end_ = max(self.details.keys())
        return int(end_)

    def set_chapter_start_end(self, chapter, start, end):
        if self.chapter is not None:
            self.start_chapter = chapter.split('/')[-1]
            self.end_chapter = chapter.split('/')[-1]
        else:
            self.start_chapter = self._get_start(start)
            self.end_chapter  = self._get_end(end)
