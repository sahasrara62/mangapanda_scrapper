import requests
from lxml import html
import os

website_url = str(r'https://www.mangapanda.com')


def get_xpath_result(url, rule):
    content = get_content(url)
    tree = html.fromstring(content)
    result = tree.xpath(rule)
    return result


def check_connection(url):
    """
    check if a web link is correct or not
    :param url:
    :return:
    """
    try:
        if requests.head(url).status_code < 400:
            print('url {} is valid'.format(url))
            return True
    except:
        print('url is invalid')
        return False


def get_response(url):
    if check_connection(url):
        return requests.get(url)
    print('Invalid link {} passing the result'.format(url))
    pass


def get_content(url):
    response = get_response(url)
    if response is not None:
        return response.content
    print('Invalid link')
    return None


rules = {'chapter': r'//*/div[@id="chapterlist"]/table[@id="listing"]/tr/td/a',
         'pages': r'//*/div[@id="selectpage"]/select[@id="pageMenu"]',
         'images': r'//*/img[@id="img"]'}


def get_chapters_data(url):
    """
    url of the page eg : https://www.mangapanda.com/one-piece
    will give the data of all the chapters, name, link and source
    :param url: url of page
    :return: list of dict
    """
    chapter_rule = rules['chapter']

    data = get_xpath_result(url, chapter_rule)
    dic = {'chapter': '', 'url': '', 'name': ''}
    result = []
    for _chapter in data:
        dic['chapter'] = _chapter.text.strip()
        dic['url'] = r'{}{}'.format(website_url, _chapter.attrib['href']).strip()
        dic['name'] = _chapter.tail.strip()
        result.append(dic)
        dic = {'chapter': '', 'url': '', 'name': ''}
    return result


def get_chapter_page_links(url):
    """
    return the no of pages in a chapter , their link , and name
    :param url: url of the chapter
    :return: list of the chapter page details
    """

    rule = rules['pages']
    data = get_xpath_result(url, rule)[0]
    page_links = {str(i + 1): r'{}{}'.format(website_url, value.attrib['value']) for i, value in enumerate(data)}
    return page_links


def get_image_from_manga_page(url):
    rule = rules['images']
    dic = {'page_name': '', 'source': ''}
    result = get_xpath_result(url, rule)
    dic['page_name'], dic['source'] = result[0].attrib['alt'].strip(), result[0].attrib['src'].strip()
    return dic


def get_page_details(chapter_url):
    print(chapter_url)
    dic = {'page_link': '', 'page_name': '', 'source': ''}
    page_details = get_chapter_page_links(chapter_url)
    print(page_details)
    result = []
    for page in page_details:
        details = get_image_from_manga_page(page_details[page])
        dic['page_link'] = page_details[page]
        dic['page_name'], dic['source'] = details['page_name'], details['source']
        result.append(dic)
        dic = {'page_link': '', 'page_name': '', 'source': ''}
    return result

def save_file(image_file, location, filename, img_format):
    image_loc = os.path.join(location, filename)+img_format
    with open(image_loc, 'wb') as file:
        file.write(image_file)
    return True if os.path.isfile(image_loc) else False
