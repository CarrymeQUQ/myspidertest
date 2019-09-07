# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from project1.items import Project1Item


client = MongoClient()
collection = client["tieba"]["tiebaspider"]

class Project1Pipeline(object):
    def process_item(self, item, spider):
        if item["poster"] is not None:
            item["poster"] = self.process_poster(item["poster"])
        if isinstance(item, Project1Item):
            print(item)
            # collection.insert(dict(item))

        return item

    def process_poster(self,poster):
        poster = poster.lstrip()
        return poster
