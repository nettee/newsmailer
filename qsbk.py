#!/usr/bin/env python3

import heapq
from datetime import date
from pathlib import Path

from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup

class QsItem(dict):

    def __init__(self, text, votes, comments):
        self['text'] = text
        self['votes'] = votes
        self['comments'] = comments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Qs<{text} - {votes} 好笑, {comments} 评论>'.format(**self)

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

    qss = []

    first_page = 'https://www.qiushibaike.com/hot/'
    crawler = CsbkCrawler(first_page, qss)

    selected_qss = heapq.nlargest(10, qss, lambda qs: qs["votes"])
    return selected_qss

def generate_mail(qs_list):

    mimetype = 'plain'
    subject = '糗事百科每日精选'
    text = '\n--------------------------\n'.join('{text}\n{votes} 好笑 {comments} 评论'.format(**qs) for qs in qs_list)

    return {
        'mimetype': mimetype,
        'subject': subject,
        'text': text
    }


if __name__ == '__main__':

    selected_qss = collect()

    for qs in selected_qss:
        print(qs)
    
    
