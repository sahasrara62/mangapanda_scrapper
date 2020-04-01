"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"
"""
import os

import requests
from lxml import html
from urllib.parse import urlparse, urljoin
import tqdm
import json


class Scrap:
    def __init__(self, url, chapter=None, start=None, end=None, location=None):
        """
        Base Scrap class which store the scrapping details


        :param url: manga page url example : https://www.mangapanda.com/one-piece
        :param chapter: chapter_url example : https://www.mangapanda.com/one-piece/1
        :param start: if a list of chapter to download
        :param end: end chapter which need to download
        :param location: location where manga chapter will be saved
        """

        self.manga_url = url
        self.chapter = chapter
        self.start_chapter = start
        self.end_chapter = end
        self.location = location  # location if not None else os.path.dirname(os.path.realpath(__file__))
        self.manga_name = urlparse(self.manga_url)[2].split('/')[1]
        self.web_url = urlparse(self.manga_url)[0] + '://' + urlparse(self.manga_url)[1]


class Download(Scrap):
    def __init__(self, url):
        super().__init__(url)
        if self.location is None:
            self.location = os.path.dirname(os.path.realpath(__file__))

    def _get_page_urls(self, chapter_url):
        """
        return the url of the pages present for that chapter 
        
        
        :param chapter_url:url of the chapter eg : "https://www.mangapanda.com/one-piece/1"
        :return: list of urls of the pages for that chapter eg ["https://www.mangapanda.com/one-piece/1".
        "https://www.mangapanda.com/one-piece/1/2" ..]
        """
        page_content = requests.get(chapter_url).content
        extract_rule = r'//*/div[@id="selectpage"]/select[@id="pageMenu"]'
        tree = html.fromstring(page_content)
        data = tree.xpath(extract_rule)[0]
        chapter_manga_page_links = [urljoin(self.web_url, '{}'.format(i.attrib['value'])) for i in data]
        return chapter_manga_page_links

    def save_manga(self, location, page_image_url, name, extension='jpeg', tqdm=tqdm):

        """
        save the chapter page images

        :param location: image file to store
        :param page_image_url: manga chapter page image url
        :param name: name of that chapter page
        :param extension: image format extension
        :return:
        """
        # Streaming, so we can iterate over the response.
        r = requests.get(page_image_url, stream=True)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        t = self.tqdm(total=total_size, unit='iB', unit_scale=True)

        ext = '.{}'.format(extension)
        manga_chapter_page = os.path.join(location, name, extension)

        if r.status_code == 200:
            try:
                with open(manga_chapter_page, 'wb') as page:
                    for data in r.iter_content(block_size):
                        t.update(len(data))
                        page.write(data)
                t.close()
            except OSError:
                print("unable to save")

        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
        return 1

    def _save_details(self, data, location, ):
        with open(os.path.join(location, '.chapter_logs'), 'w+') as f:
            print(data)
            f.write(json.dumps(data))

    def dowload_manga(self, urls, location, extension='jpeg'):

        """

        :param urls: list of all page urls
        :param location: where the chapter need to be saved
        :return: None
        """
        data = {}

        for index, page_url in enumerate(urls):
            dic = {'page_name': '', 'image_source': ''}
            res = requests.get(page_url).content
            path = r'//*/img[@id="img"]'
            tree = html.fromstring(res)
            result = tree.xpath(path)
            dic['page_name'], dic['image_source'] = result[0].attrib['alt'], result[0].attrib['src']
            self.save_manga(location, dic['image_source'], dic['page_name'], extension=extension)
            data.update(dic)

        self._save_details(location, data)
        return 1

    def get_chapters_details(self):

        response = requests.get(self.manga_url).content
        tree = html.fromstring(response)
        path = r'//*/div[@id="chapterlist"]/table[@id="listing"]/tr/td/a'
        res = tree.xpath(path)
        dic = {'chapter': '', 'url': ''}
        result = {}
        for chapter_number, chapter_details in enumerate(res):
            dic['chapter_name'] = "{} {}".format(chapter_details.text, chapter_details.tail)
            dic['url'] = self.manga_url + chapter_details.attrib['href']
            # dic['name'] = chapter_details.tail
            result.update({str(chapter_number + 1): dic})
            dic = {'chapter': '', 'url': ''}
        self._save_details( result, self.location)
        return result




