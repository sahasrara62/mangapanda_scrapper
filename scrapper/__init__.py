"""
__author__ = "prashant rana"
__email__ = "uchiha.rana62@gmail.com"

This is scrapper module which do all the work of scrapping, maintaining data and storing the information.
"""

from .scrap import Download, Scrap
from .create import Create


class MangaDownload:
    def download_manga(chapter=None, location=None, start=None, end=None, url=None):
        scrapper = Scrap(url,chapter=chapter, location=location, start=start, end=end)

        file_creator = Create(scrapper.manga_name, scrapper.location)

        manga_path = file_creator.pro_dir

        scrapper.location = manga_path

        manga_details = scrapper.details
        scrapper.save_details(manga_details, manga_path)
        print(scrapper.start_chapter, scrapper.end_chapter)
        for data in range(int(scrapper.start_chapter), int(scrapper.end_chapter) + 1):
            name, link = manga_details[data]['chapter_name'], manga_details[data]['url']
            print(name, link)
            chapter_page_link = scrapper.get_page_urls(link)
            folder = file_creator.create_directory(name, manga_path)

            scrapper.download_manga(chapter_page_link, folder)


download_manga = MangaDownload.download_manga
