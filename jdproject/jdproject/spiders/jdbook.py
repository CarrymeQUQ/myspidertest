# -*- coding: utf-8 -*-
import scrapy
import urllib
from copy import deepcopy
import json


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 分组
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")

            # 小分组
            for em in em_list:
                item["s_cate"] = em.xpath("./a/text()").extract_first()
                item["s_href"] = em.xpath("./a/@href").extract_first()
                if item["s_href"] is not None:
                    item["s_href"] = "https:" + item["s_href"]
                    # print(item)
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@source-data-lazy-img").extract_first()

            item["book_img"] = "https:" + item["book_img"] if item["book_img"] is not None else None
            item["book_href"] = li.xpath(".//div[@class='p-img']/a/@href").extract_first()
            if item["book_href"] is not None:
                item["book_href"] = "https:" + item["book_href"] if item["book_href"] is not None else None
            item["book_author"] = li.xpath(".//span[@class='author_type_1']/a/text()").extract()
            item["book_press"] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract_first()
            item["book_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
            book_data_sku = li.xpath("./div/@data-sku").extract_first()
            # print(item)
            if book_data_sku is not None:
                yield scrapy.Request(
                    "https://p.3.cn/prices/mgets?&skuIds=J_{}".format(book_data_sku),
                    callback=self.parse_book_prices,
                    meta={"item": deepcopy(item)}
                )
        # 翻页
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )

    def parse_book_prices(self, response):
        item = response.meta["item"]
        item["book_prices"] = json.loads(response.body.decode())[0]["op"]
        yield item