# -*- coding: utf-8 -*-
import scrapy
import re

# 这种方式是在form 表单中有action地址的前提下
class GithubFromResponseSpider(scrapy.Spider):
    name = 'github_from_response'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):

        yield scrapy.FormRequest.from_response(
            response,  # 自动的从response响应中寻找form 表单
            formdata={"login":"RookieWithNoob", "password":"nvli5201314"},
            callback = self.parse_index,
        )

    def parse_index(self, response):
        print(re.findall(r"RookieWithNoob", response.body.decode()))
        print("*" * 50)
        print(response.url, "*"*30, response.status)