# -*- coding: utf-8 -*-
import scrapy
from project1.items import Project1Item
import re


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E7%BE%8E%E5%A5%B3']

    def parse(self, response):
        # 分组
        li_list = response.xpath("//ul[@class='threads_list']/li[@class='tl_shadow tl_shadow_new ']")
        # print(li_list)
        for li in li_list:
            item = Project1Item()
            item["title"] = li.xpath("./a/div[@class='ti_title']/span/text()").extract_first()
            item["href"] = "https://tieba.baidu.com" + li.xpath("./a/@href").extract_first()
            item["poster"] = li.xpath(".//span[@class='ti_author']/text()").extract_first()
            item["reply_num"] = li.xpath(".//span[@class='btn_icon']/text()").extract_first()
            item["datetime"] = li.xpath(
                ".//span[@class='ti_time']/text()").extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"},
                meta={"item": item}
            )

        # 提取下一页地址
        current_page = int(re.findall(r"\"current_page\":(.*?),", response.body.decode("utf-8"), re.S)[0])
        total_page = int(re.findall(r"\"total_page\":(.*?),", response.body.decode("utf-8"), re.S)[0])
        # print(current_page)
        # print(total_page)
        if current_page < total_page:
            yield scrapy.Request(
                TiebaSpider.start_urls[0] + "&pn={}&".format(current_page*30),
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["img_list"] = response.xpath("//div[@class='d_post_content_main  d_post_content_firstfloor']//div[@class='d_post_content j_d_post_content ']/img/@src").extract()
        yield item
