# -*- coding: utf-8 -*-
import scrapy
from project2.items import Project2Item
from copy import deepcopy
import re


class SnSpider(scrapy.Spider):
    name = 'sn'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/?safp=d488778a.10038.searchPathbox.1']

    def parse(self, response):
        # # 分组

        # item_list = response.xpath("//div[@class='menu-list']/div[@class='menu-item']")
        # # print(item_list)
        # for div in item_list:
        #     item["b_cate"] = div.xpath(".//h3/a/text()").extract_first()
        #     # print(item["b_cate"])

        # 大分类
        div_list = response.xpath("//div[@class='menu-list']/div[@class='menu-sub']/div[@class='submenu-left']")[0:-1]
        # 小分类
        for div in div_list:
            item = Project2Item()
            # 大分类
            # ul_list = div.xpath("./ul")

            p_list = div.xpath("./p") if len(div.xpath("./p"))>0 else None
            # print(p_list)
            if p_list is not None:
                for p in p_list:
                    item["m_cate"] = p.xpath("./a/text()").extract_first()
                    # print(item["m_cate"])
                    li_list = p.xpath("./following-sibling::ul[1]/li")
                    # for ul in ul_list:
                    #     li_list = ul.xpath("./li")
                    # 小分类
                    for li in li_list:
                        item["s_cate"] = li.xpath("./a/text()").extract_first()
                        # print(item["s_cate"])
                        item["s_href"] = li.xpath("./a/@href").extract_first()
                        # print(item["s_href"])
                        # print(item)
                        if item["s_href"] is not None:
                            yield scrapy.Request(
                                item["s_href"],
                                callback=self.parse_book_list,
                                meta={"item": deepcopy(item)}
                            )
            if p_list is None:
                item["m_cate"] = None
                ul_list = div.xpath("./ul")
                for ul in ul_list:
                    li_list = ul.xpath("./li")
                # 小分类
                    for li in li_list:
                        item["s_cate"] = li.xpath("./a/text()").extract_first()
                        # print(item["s_cate"])
                        item["s_href"] = li.xpath("./a/@href").extract_first()
                        # print(item["s_href"])
                        # print(item)
                        if item["s_href"] is not None:
                            yield scrapy.Request(
                                item["s_href"],
                                callback=self.parse_book_list,
                                meta={"item": deepcopy(item)}
                            )



    def parse_book_list(self, response):
        item = response.meta["item"]
        # 图书列表页分组
        book_list = response.xpath("//div[@id='filter-results']/ul/li")
        # print(book_list)
        for book in book_list:
            item["book_name"] = book.xpath(".//div[@class='img-block']//img/@alt").extract_first()
            # print(item["book_name"])
            item["book_img_url"] = book.xpath(".//div[@class='img-block']//img/@src").extract_first()
            if item["book_img_url"] is None:
                item["book_img_url"] = book.xpath(".//div[@class='img-block']//img/@src2").extract_first()
            item["book_img_url"] = "https:" + item["book_img_url"]
            item["book_href"] = book.xpath(".//div[@class='img-block']/a/@href").extract_first()
            if item["book_href"] is not None:
                item["book_href"] = "https:" + item["book_href"]
                # print(item["book_href"])
                # print(item)
                yield scrapy.Request(
                    item["book_href"],
                    callback=self.parse_book_detail,
                    meta={"item": deepcopy(item)}
                )
        # 翻页
        # print(response.body.decode())
        currentPage = int(re.findall("param.currentPage = \"(.*?)\";", response.body.decode())[0])
        currentPage += 1
        # print(currentPage)
        pageNumbers = int(re.findall("param.pageNumbers = \"(.*?)\";", response.body.decode())[0])
        if currentPage<pageNumbers:
            # next_url = response.xpath("//a[@class='cur']/following-sibling::a[1]/@href").extract_first()
            # next_url = "https://list.suning.com" + next_url
            b = list(item["s_href"])
            b[33] = str(currentPage)
            next_url = "".join(b)
            # print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )


    def parse_book_detail(self, response):
        item = response.meta["item"]
        item["book_author"] = response.xpath("//ul[@class='bk-publish clearfix']/li[1]/text()").extract_first()
        item["book_publish"] = response.xpath("//ul[@class='bk-publish clearfix']/li[2]/text()").extract_first()
        item["book_date"] = response.xpath("//ul[@class='bk-publish clearfix']/li[3]/span[2]/text()").extract_first()
        # print(item)
        yield item
