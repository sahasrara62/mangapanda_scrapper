import os

import requests
from lxml import html

from cleanname import clean_filename


website_url = r'https://www.mangapanda.com'



def check_url(url):
    url_status = requests.head(url)
    if url_status.status_code < 400:
        return True
    return False


def scrap_chapter_list(url, respose):
    dic = {'chapter': '', 'name': '', 'link': ''}

    # start scrapping
    # soup  = BeautifulSoup(respose.text,'html.parser')
    tree = html.fromstring(respose.content)
    return None


def get_list_of_chapers(url):
    if check_url(url):
        response = requests.get(url).content
        tree = html.fromstring(response)
        path = r'//*/div[@id="chapterlist"]/table[@id="listing"]/tr/td/a'
        res = tree.xpath(path)
        dic = {'chapter': '', 'url': '', 'name': ''}
        result = []
        for i in res:
            dic['chapter'] = i.text
            dic['url'] = website_url + i.attrib['href']
            dic['name'] = i.tail
            result.append(dic)
            dic = {'chapter': '', 'url': '', 'name': ''}
        return result
    return None


def get_page_list(chapter_url):
    res = requests.get(chapter_url).content
    path = r'//*/div[@id="selectpage"]/select[@id="pageMenu"]'
    tree = html.fromstring(res)
    data = tree.xpath(path)[0]
    page_links = ['{}'.format(i.attrib['value']) for i in data]
    return page_links


def get_image_from_page(url):
    """

    :param url:  url of the given manga page eg. /one-piece/1/1
    :return: name of the page(manga name, link to the image file
    """
    dic = {'page_name': '', 'source': ''}
    page_url = r'{}{}'.format(website_url, url)
    res = requests.get(page_url).content
    path = r'//*/img[@id="img"]'
    tree = html.fromstring(res)
    result = tree.xpath(path)
    dic['page_name'], dic['source'] = result[0].attrib['alt'], result[0].attrib['src']
    return dic


def download_image(image_url):
    image_file = requests.get(image_url).content
    return image_file


def save_file(image_file, path):
    image_loc = path
    with open(image_loc, 'wb') as file:
        file.write(image_file)
    return True if os.path.isfile(image_loc) else False


def get_page_details(chapter_url):
    dic = {'page_link': '', 'page_name': '', 'source': ''}
    page_details = get_page_list(chapter_url)
    result = []
    for page in page_details:
        details = get_image_from_page(page)
        dic['page_link'] = page
        dic['page_name'], dic['source'] = details['page_name'], details['source']
        result.append(dic)
        dic = {'page_link': '', 'page_name': '', 'source': ''}
    return result



manga_url = r'' # give manag link here eg 'https://www.mangapanda.com/one-piece'
storing_location = r'' # give location for the storing the manga here 
manga_name = manga_url.split('/')[-1]
location = os.path.join(storing_location, clean_filename(manga_name))
chapter_list = get_list_of_chapers(manga_url)

if not os.path.exists(location):
    print('creating the folder {}'.format(manga_name))
    os.makedirs(location)

for chapter in chapter_list:
    name = r'{} {}'.format(chapter['chapter'], chapter['name']).strip()
    print(name)
    chapter_path = os.path.join(location,clean_filename(name)) # clean_filename(name))
    print(chapter_path)
    if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)
    chapter_details = get_page_details(chapter['url'])
    for _page in chapter_details:
        name, src = _page['page_name'], _page['source']
        img_format = '.' + src.split('.')[-1]
        print('saving image {} in path {}'.format(name, chapter_path))
        image_data = requests.get(src).content

        path = os.path.join(chapter_path.strip(), clean_filename(name)) + img_format
        if not os.path.isfile(path):
            open(path, 'a').close()
            if os.path.isfile(path):
                print("file created {}".format(path))
        
        save_file(image_data, path)
