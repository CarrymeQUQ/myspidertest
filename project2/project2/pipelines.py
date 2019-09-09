# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from project2.items import Project2Item
import re
from pymongo import MongoClient

client = MongoClient()


class Project2Pipeline(object):
    def open_spider(self, spider):

        self.collection = client[spider.settings.get("DB")][spider.settings.get("COLLECTION")]

    def process_item(self, item, spider):
        if isinstance(item, Project2Item):
            item["book_author"] = self.process_content(item["book_author"])
            item["book_publish"] = self.process_content(item["book_publish"])
            print(item)
            self.collection.insert(dict(item))
        return item

    def process_content(self, content):
        if content is not None:
            content = re.sub(r"\s", "",content)
            # 去除字符串中的空字符串
        return content
