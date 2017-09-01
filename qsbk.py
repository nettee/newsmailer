#!/usr/bin/env python3

import heapq
from datetime import date
from pathlib import Path

from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup

class QsItem:

    def __init__(self, text, votes, comments):
        self.text = text
        self.votes = votes
        self.comments = comments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}\n{} 好笑, {} 评论'.format(self.text, self.votes, self.comments)

    def toJson(self):
        return '''{{
    "text": "{}",
    "votes": "{}",
    "comments": "{}"
}}'''.format(self.text, self.votes, self.comments)

class QsList(list):

    def toJson(self):
        return '''[
    {}
]'''.format(',\n    '.join(qs.toJson() for qs in self))

class CsbkCrawler:

    def __init__(self, page, qs_list):
        self.page = page
        res = requests.get(page)
        res.raise_for_status()
        html = BeautifulSoup(res.text, 'lxml')
        self.crawl_page(html, qs_list)
        next_ = html.find('span', class_='next')
        next_string = next_.get_text().strip()
        if next_string == '下一页':
            next_page = next_.parent['href']
            next_page = urljoin(page, next_page)
            crawler = CsbkCrawler(next_page, qs_list)

    def crawl_page(self, html, qs_list):
        content = html.find('div', id='content-left')
        articles = content.find_all('div', class_='article')
        for article in articles:
            a = article.find('a', recursive=False)
            text = a.find('div', class_='content').find('span').get_text().strip()
            thumb = article.find('div', class_='thumb', recursive=False)
            if thumb is not None:
                continue # omit qs with pictures currently
            stats = article.find('div', class_='stats', recursive=False)
            span_vote = stats.find('span', class_='stats-vote').find('i', class_='number')
            votes = int(span_vote.get_text().strip())
            span_comment = stats.find('span', class_='stats-comments').find('i', class_='number')
            comments = int(span_comment.get_text().strip())
            qs = QsItem(text, votes, comments)
            qs_list.append(qs)

def collect():

    qss = QsList()

    first_page = 'https://www.qiushibaike.com/hot/'
    crawler = CsbkCrawler(first_page, qss)

    selected_qss = heapq.nlargest(10, qss, lambda qs: qs.votes)
    qss2 = QsList()
    qss2.extend(selected_qss)
    return qss2

def collect_text():

    today = date.today().strftime('%Y%m%d')
    print('today:', today)

    p = Path('data/qsbk-{}.txt'.format(today))
    if p.is_file():
        print('have file')
        with p.open('r') as f:
            return f.read()
    else:
        print('no file')
        qss = collect()
        text = '\n---------------------------------------\n'.join(str(qs) for qs in qss)
        with p.open('w') as f:
            print(text, file=f)
        return text
    
if __name__ == '__main__':

    selected_qss = collect()

    for qs in selected_qss:
        print(qs)
    
    
