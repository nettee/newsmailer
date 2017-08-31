#!/usr/bin/env python3

from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup

class CsbkCrawler:

    def __init__(self, page):
        print(page)
        self.page = page
        res = requests.get(page)
        res.raise_for_status()
        html = BeautifulSoup(res.text, 'lxml')
        next_ = html.find('span', class_='next')
        next_string = next_.get_text().strip()
        if next_string == '下一页':
            next_page = next_.parent['href']
            next_page = urljoin(page, next_page)
            crawler = CsbkCrawler(next_page)


if __name__ == '__main__':

    first_page = 'https://www.qiushibaike.com/hot/'
    crawler = CsbkCrawler(first_page)
    
    
