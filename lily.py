#!/usr/bin/env python3

import time
import re
from urllib.parse import urljoin
import json

import requests
from bs4 import BeautifulSoup
import jinja2

abbr = 'lily'

class TopItem(dict):

    def __init__(self, rank, board, title, link, comments):
        self['rank'] = rank
        self['board'] = board
        self['title'] = title
        self['link'] = link
        self['comments'] = comments
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Top<[{rank}] {title} ({comments})>'.format(**self)

def collect_abstract():

    abstract = []

    page = 'http://bbs.nju.edu.cn/bbstop10'

    res = requests.get(page)
    res.raise_for_status()
    html = BeautifulSoup(res.text, 'lxml')

    table = html.find('table')
    top10 = table.find_all('tr')[1:]
    for item in top10:
        tds = item.find_all('td')
        rank = tds[0].string.strip()
        board = tds[1].string.strip()
        title = tds[2].string.strip()
        link = tds[2].find('a')['href']
        link = urljoin(page, link)
        comments = int(tds[4].string.strip())
        ti = TopItem(rank, board, title, link, comments)
        abstract.append(ti)

    return abstract

def collect_details(abstract):

    for item in abstract:
        url = item['link']
        res = requests.get(url)
        res.raise_for_status()

        m = re.search('\[本篇人气: (\d+)\]', res.text)
        pop = int(m.group(1)) if m is not None else None
        item['pop'] = pop

        # Anti-crawler strategy aborts the 10th request.
        time.sleep(1)

    return abstract

def collect():

    return collect_details(collect_abstract())

def generate_mail(top_list, date_string):

    mimetype = 'html'
    subject = '小百合每日十大 {}'.format(date_string)

    template = jinja2.Template('''<html>
<body>
    <h3>摘要</h3>
    <p>
    {% for top in top_list %}
    {{ loop.index }}. 
    <a href="{{ top.link }}">{{ top.title }}</a>
    (评论:{{ top.comments }} | 人气:{{ top['pop'] }}) 
    <br />
    {% endfor %}
    </p>
</body>
</html>''')
    body = template.render(top_list=top_list)

    return {
        'mimetype': mimetype,
        'subject': subject,
        'body': body
    }

if __name__ == '__main__':

    details = collect()
    print(json.dumps(details))



