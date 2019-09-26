# -*- coding: utf-8 -*-
import scrapy
from bosszhipin.items import BosszhipinItem
from copy import deepcopy
from urllib import parse
import time


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/']

    def parse(self, response):
        print(response.headers)
        print(response.request.headers)
        print("***")
        item = BosszhipinItem()

        # 大分组
        div_list = response.xpath("//div[@class='job-menu' or @class='all-box']/dl/div[@class='menu-sub']")
        for div in div_list:
            item["b_cate"] = div.xpath("./p/text()").extract_first()
            # 小分类
            li_list = div.xpath("./ul/li")
            for li in li_list:
                item["m_cate"] = li.xpath("./h4/text()").extract_first()
                # 小小分类
                a_list = li.xpath("./div/a")
                for a in a_list:
                    item["s_cate"] = a.xpath("./text()").extract_first()
                    item["s_href"] = a.xpath("./@href").extract_first()
                    # cookies = "__c=1569417162; __g=-; __l=l=%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DDvJ3Azo3b2r6Xm45fL8UGpiVwApKYgMkMhUirvy2mR4%253D%26name%3Dfc9b69f9%26ts%3D1569417065297%26callbackUrl%3D%252Fc101200100-p230201%252F%26srcReferer%3Dhttps%253A%252F%252Fwww.zhipin.com%252F&r=&friend_source=0".format(
                    #     int(time.time()))
                    # cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
                    if item["s_href"] is not None:
                        item["s_href"] = parse.urljoin(response.url, item["s_href"])

                        yield scrapy.Request(
                            item["s_href"],
                            # cookies=cookies,
                            callback=self.parse_content,
                            meta={"item": deepcopy(item)}
                        )


    def parse_content(self, response):
        item = response.meta["item"]
        print(item["s_href"])
        print("***")
        print(response.url)
        # 分组
        li_list = response.xpath("//div[@class='job-list']/ul/li")

        print(li_list)
        for li in li_list:
            item["title"] = li.xpath(".//div[@class='info-primary']/h3/a/div[@class='job-title']/text()").extract_first()
            item["href"] = li.xpath(".//div[@class='info-primary']/h3/a/@href").extract_first()
            if item["s_href"] is not None:
                item["s_href"] = parse.urljoin(response.url, item["s_href"])
            item["wage"] = li.xpath(".//div[@class='info-primary']/h3/a/span/text()").extract_first()
            item["addr"] = li.xpath(".//div[@class='info-primary']/p/text()").extract_first()
            item["company"] = li.xpath(".//div[@class='info-company']/div/h3/a/text()").extract_first()
            item["company_detail"] = li.xpath(".//div[@class='info-company']/div/p/text()").extract_first()
            item["hr_name"] = li.xpath(".//div[@class='info-publis']/h3/text()").extract_first()
            item["date"] = li.xpath(".//div[@class='info-publis']/p/text()").extract_first()
            # print(item)
            # yield item
