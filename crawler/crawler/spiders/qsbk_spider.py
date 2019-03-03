from urllib.parse import urljoin

import scrapy

from crawler.items import QsbkItem


class QsbkSpider(scrapy.Spider):

    name = 'qsbk'
    allowed_domains = [
        'qiushibaike.com',
    ]
    start_urls = [
        'https://www.qiushibaike.com/hot/',
    ]

    def parse(self, response):
        print('URL:', response.request.url)

        # Find jokes
        content = response.css('div#content-left')
        articles = content.css('div.article')
        for article in articles:
            href = article.css('a.contentHerf::attr(href)').extract_first()
            link = urljoin(response.request.url, href)

            lines = article.css('div.content span::text').extract()
            text = '\n'.join(line.replace('\n', '') for line in lines)

            thumb = article.css('div.thumb')
            if thumb:
                imgs = thumb.css('img.illustration::attr(src)').extract()
                img_urls = [urljoin(response.request.url, img) for img in imgs]
            else:
                img_urls = []

            stats = article.css('div.stats')
            votes = stats.css('span.stats-vote .number::text').extract_first()
            votes = int(votes)
            comments = stats.css('span.stats-comments .number::text').extract_first()
            comments = int(comments)

            yield QsbkItem(link=link, text=text, img_urls=img_urls, votes=votes, comments=comments)

        # Find next page
        hrefs = response.css('a:contains(下一页)::attr(href)').extract()
        for href in hrefs:
            next_url = urljoin(response.request.url, href)
            yield scrapy.Request(url=next_url, callback=self.parse)
