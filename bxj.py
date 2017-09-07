#!/usr/bin/env python3

import time
from datetime import date, timedelta

import re
from urllib.parse import urljoin
import json
import heapq

import requests
from bs4 import BeautifulSoup
import jinja2

abbr = 'bxj'

class PostItem(dict):

    def __init__(self, title, link, lights, postdate, comments, views):
        self['title'] = title
        self['link'] = link
        self['lights'] = lights
        self['date'] = postdate
        self['comments'] = comments
        self['views'] = views

    def index(self):
        return self['comments']

    def __lt__(self, other):
        return self.index() < other.index()

class PostRanker:

    def __init__(self, limit):
        self.limit = limit
        self.posts = []
        self.count = 0

    def add(self, item):
        if self.count < self.limit:
            heapq.heappush(self.posts, item)
        else:
            heapq.heappush(self.posts, item)
            heapq.heappop(self.posts)
        self.count += 1

    def getResult(self):
        result = []
        for __ in range(len(self.posts)):
            post = heapq.heappop(self.posts)
            result.insert(0, post)
        return result

def collect():

    today = date.today()

    postRanker = PostRanker(20)

    first_page = 'https://bbs.hupu.com/bxj-postdate'
    pns = 10
    for pn in range(0, pns): 
        page = first_page if pn == 0 else '{}-{}'.format(first_page, pn+1)
        print(page)
        res = requests.get(page)
        res.raise_for_status()
        html = BeautifulSoup(res.text, 'lxml')
        body = html.find('div', class_='show-list')
        posts = body.find('ul', class_='for-list').find_all('li')
        for post in posts:
            titlelink = post.find('div', class_='titlelink').find('a')
            title = titlelink.string.strip()
            link = urljoin(page, titlelink['href'])
            light_r = titlelink.find_next_sibling('span', class_='light_r')
            if light_r is not None:
                text = light_r.find('a')['title']
                m = re.search('(\d+)', text)
                lights = int(m.group(1)) if m is not None else 0
            else:
                lights = 0
            date_string = post.find('div', class_='author').find_all('a')[1].string.strip()
            postdate = date(*[int(d) for d in date_string.split('-')])
            postdate_string = postdate.strftime('%Y-%m-%d')

            stats = post.find('span', class_='ansour').string.strip()
            comments, views = [int(s.strip()) for s in stats.split('/')]
            postItem = PostItem(title, link, lights, postdate_string, comments, views)
            postRanker.add(postItem)

        # In case of anti-crawler
        time.sleep(1)

    return postRanker.getResult()

def generate_mail(posts, date_string):

    mimetype = 'html'
    subject = '虎扑步行街精选 {}'.format(date_string)

    template = jinja2.Template('''<html>
<body>
    {% for post in posts %}
        <h3>第 {{ loop.index }} 名</h3>
        <p>
        <a href="{{ post.link }}">{{ post.title }}</a>
        </p>
        <p>浏览:{{ post.views }} | 评论:{{ post.comments }} | 亮了:{{ post.lights }}</p>
        {% if not loop.last %}
        <hr />
        {% endif %}
    {% endfor %}
</body>
</html>''')

    body = template.render(posts=posts)

    return {
        'mimetype': mimetype,
        'subject': subject,
        'body': body
    }

if __name__ == '__main__':

    posts = collect()
    print(json.dumps(posts))
