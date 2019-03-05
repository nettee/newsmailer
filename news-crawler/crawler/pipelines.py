# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from crawler.db.dbhelper import DbHelper


class DatabasePipeline(object):

    def __init__(self):
        self.db = DbHelper()

    def process_item(self, item, spider):
        if spider.name == 'qsbk':
            self.db.insert_qsbk(item)
        return item
