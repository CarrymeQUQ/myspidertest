# -*- coding: utf-8 -*-
import scrapy
import re


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    # 第一种　　携带登录后的cookie登录 重写父类的start_requests方法
    # def start_requests(self):
    #     cookies = "anonymid=jcokuqturos8ql; depovince=GW; jebecookies=f90c9e96-78d7-4f74-b1c8-b6448492995b|||||; _r01_=1; JSESSIONID=abcx4tkKLbB1-hVwvcyew; ick_login=ff436c18-ec61-4d65-8c56-a7962af397f4; _de=BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5; p=90dea4bfc79ef80402417810c0de60989; first_login_flag=1; ln_uact=mr_mao_hacker@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20171230/1635/main_JQzq_ae7b0000a8791986.jpg; t=24ee96e2e2301bf2c350d7102956540a9; societyguester=24ee96e2e2301bf2c350d7102956540a9; id=327550029; xnsid=e7f66e0b; loginfrom=syshome; ch_id=10016"
    #     cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
    #     # headers = {"Cookie":cookies}
    #     yield scrapy.Request(
    #         self.start_urls[0],
    #         callback=self.parse,
    #         cookies=cookies
    #         # headers = headers
    #     )

    # 第二种　scrapy.FormRequest(校验地址url, 请求体formdata, callback回调函数)
    def parse(self, response):
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        utf8 = response.xpath("//input[@name='utf8']/@value").extract_first()
        commit = response.xpath("//input[@name='commit']/@value").extract_first()
        required_field = response.xpath("//input[@class='form-control'][1]/@name").extract_first()
        timestamp = response.xpath("//input[@name='timestamp']/@value").extract_first()
        timestamp_secret = response.xpath("//input[@name='timestamp_secret']/@value").extract_first()
        post_date = dict(
            login="RookieWithNoob",
            password="nvli5201314",
            authenticity_token=authenticity_token,
            utf8=utf8,
            commit=commit,
            timestamp=timestamp,
            timestamp_secret=timestamp_secret,
        )
        post_date[required_field] = ""

        # print(post_date)
        yield scrapy.FormRequest(
            "https://github.com/session",
            formdata=post_date,
            callback=self.parse_index,

        )

    def parse_index(self, response):
        print(re.findall(r"RookieWithNoob", response.body.decode()))
        print(response.url, "****", response.status)
