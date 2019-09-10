# -*- coding: utf-8 -*-
import scrapy
from project4.items import Project4Item
from copy import deepcopy


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.com']
    start_urls = ['http://tieba.baidu.com/f?&kw=python']

    def parse(self, response):
        item = Project4Item()
        # 分组
        # li_list = response.xpath("//ul[@id='thread_list']/li[@class=' j_thread_list clearfix']")
        # for li in li_list:
        #     item["title"] = li.xpath(".//div[@class='threadlist_lz clearfix']//a[@class='j_th_tit']/text()").extract_first()
        #     item["author"] = li.xpath(".//div[@class='threadlist_lz clearfix']/div[@class='threadlist_author pull_right']/span[1]/@title").extract_first()
        #     item["create_time"] = li.xpath(".//div[@class='threadlist_lz clearfix']/div[@class='threadlist_author pull_right']/span[2]/text()").extract_first()
        #     item["rep_num"] = li.xpath(".//div[@class='col2_left j_threadlist_li_left']/span[@title='回复']/text()").extract_first()
        #     item["last_reply_name"] = li.xpath(".//div[@class='threadlist_detail clearfix']/div[@class='threadlist_author pull_right']/span[1]/@title").extract_first()


