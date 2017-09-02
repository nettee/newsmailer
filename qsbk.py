#!/usr/bin/env python3

import heapq
from datetime import date
from pathlib import Path

from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup

class QsItem(dict):

    def __init__(self, url, text, votes, comments):
        self['url'] = url
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
        self.crawl_page(page, html, qs_list)
        next_ = html.find('span', class_='next')
        next_string = next_.get_text().strip()
        if next_string == '下一页':
            next_page = next_.parent['href']
            next_page = urljoin(page, next_page)
            crawler = CsbkCrawler(next_page, qs_list)

    def crawl_page(self, page_url, html, qs_list):
        content = html.find('div', id='content-left')
        articles = content.find_all('div', class_='article')
        for article in articles:
            a = article.find('a', recursive=False)
            link = urljoin(page_url, a['href'])
            text = a.find('div', class_='content').find('span').get_text().strip()
            thumb = article.find('div', class_='thumb', recursive=False)
            if thumb is not None:
                continue # omit qs with pictures currently
            stats = article.find('div', class_='stats', recursive=False)
            span_vote = stats.find('span', class_='stats-vote').find('i', class_='number')
            votes = int(span_vote.get_text().strip())
            span_comment = stats.find('span', class_='stats-comments').find('i', class_='number')
            comments = int(span_comment.get_text().strip())
            qs = QsItem(link, text, votes, comments)
            qs_list.append(qs)

def collect():

    qss = []

    first_page = 'https://www.qiushibaike.com/hot/'
    crawler = CsbkCrawler(first_page, qss)

    selected_qss = heapq.nlargest(10, qss, lambda qs: qs["votes"])
    return selected_qss

def generate_mail(qs_list, date_string):

    mimetype = 'html'
    subject = '糗事百科每日精选 {}'.format(date_string)
    body = '''<html><body>
{}
</body></html>'''.format(
        '<hr />\n'.join(
            '''<h4 align="center">{}</h4>
<p text-indent="2em">{text}</p>
<p>{votes} 好笑 {comments} 评论 
    <a href="{url}">查看原文</a>
</p>\n'''.format(i+1, **qs) 
            for (i, qs) in enumerate(qs_list)))

    return {
        'mimetype': mimetype,
        'subject': subject,
        'body': body
    }


if __name__ == '__main__':

    selected_qss = collect()

    for qs in selected_qss:
        print(qs)
    
    
