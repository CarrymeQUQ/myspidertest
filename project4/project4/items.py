# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Project4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    rep_num = scrapy.Field()
    last_reply_name = scrapy.Field()
    last_reply_date = scrapy.Field()
