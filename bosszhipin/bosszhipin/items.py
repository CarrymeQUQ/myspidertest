# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BosszhipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    b_cate = scrapy.Field()
    m_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()

    title = scrapy.Field()
    href = scrapy.Field()
    wage = scrapy.Field()
    addr = scrapy.Field()
    hr_name = scrapy.Field()
    company = scrapy.Field()
    company_detail = scrapy.Field()
    date = scrapy.Field()


