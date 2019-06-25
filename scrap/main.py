import os

from .cleanname import clean_filename
from .mangapanda import get_chapters_data, get_chapter_page_links, get_page_details, get_content, save_file


class Mangapanda(object):

    def __init__(self, url, location, start=0, end=0):
        self.url = url
        self.manga_name = url.split('/')[-1]
        self.location = self._location(location)
        self.start = start
        self.end = end

    def __chapters_data(self):
        chapter_data = get_chapters_data(self.url)
        return chapter_data

    def __get_page_details(self, url):
        page_details = get_chapter_page_links(url)
        return page_details

    def __get_image_details(self, chapter_url):
        chap_imag_details = get_page_details(chapter_url)
        return chap_imag_details

    def _location(self, location):
        if os.path.exists(location):
            if os.path.exists(os.path.join(location, self.manga_name)):
                print('manga {} folder name exists'.format(self.manga_name))
            else:
                print('creating folder {} at location {}'.format(self.manga_name, location))
        else:
            print('creating location {}'.format(location))
            os.makedirs(location)
            print('creating manga folder {}'.format(self.manga_name))
            os.makedirs(os.path.join(location, self.manga_name))
        return os.path.join(location, self.manga_name)

    def download(self):
        chapter_data = self.__chapters_data()

        if self.start <= 0 or self.end <=0:
            self.start = 1
            self.end = len(chapter_data)
            print('enter valid manga number from 1 to {}'.format(len(chapter_data)))
        for i in range(self.start, self.end + 1):
            chapter = chapter_data[i]
            name = r'{} {}'.format(chapter['chapter'], chapter['name'])
            print(name)
            chapter_path = os.path.join(self.location, clean_filename(name))
            print(chapter_path)
            if not os.path.exists(chapter_path):
                os.makedirs(chapter_path)
            chapter_details = get_page_details(chapter['url'])
            for _page in chapter_details:
                name, src = _page['page_name'], _page['source']
                img_format = '.' + src.split('.')[-1]
                print('saving image {} in path {}'.format(name, chapter_path))
                image_data = get_content(src)
                save_file(image_data, chapter_path, name, img_format)
