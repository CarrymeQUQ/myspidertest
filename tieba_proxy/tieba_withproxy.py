import requests
from lxml import etree
import json
import re
import os
import time


class TiebaSpider:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.start_url = "https://tieba.baidu.com/f?ie=utf-8&kw=" + tieba_name + "&pn={}&"
        self.add_url = "https://tieba.baidu.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
        self.headers2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}

        self.PROXY_POOL_URL = 'http://localhost:5555/random'

    def get_proxy(self):
        try:
            response = requests.get(self.PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def get_proxies(self):
        proxy = self.get_proxy()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }

        return proxies

    def parse_url(self, url):
        proxies = self.get_proxies()
        print(proxies)
        response = requests.get(url, headers=self.headers, proxies=proxies, verify=False)
        html_str = response.content.decode()
        return html_str

    def parse_url_detail(self, url):
        proxies = self.get_proxies()
        print(proxies)
        response = requests.get(url, headers=self.headers2, proxies=proxies, verify=False)
        html_str = response.content.decode()
        return html_str

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//a[@data-thread-type='0']")  # 根据div分组
        # print(div_list)
        content_list = []
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./div[@class='ti_title']/span/text()")[0] if len(
                div.xpath("./div[@class='ti_title']/span/text()")) > 0 else None
            # print(div.xpath("./div[@class='ti_title']/span/text()")[0])
            item["href"] = self.add_url + div.xpath("./@href")[0] if len(
                div.xpath("./@href")) > 0 else None
            item["img_list"] = self.get_img_list(item["href"], [])
            # print(item)
            content_list.append(item)
        # print(content_list)

        return content_list

    def get_next_paper(self, html_str):
        current_page = re.findall(r"\"current_page\":(.*?),", html_str, re.S)[0]
        total_page = re.findall(r"\"total_page\":(.*?),", html_str, re.S)[0]
        return current_page, total_page

    def get_img_list(self, detail_url, total_img_list):  # detail_url就是item["href"]
        """帖子中的所有图片"""
        # 1.请求列表页的url 获取详情页的第一页
        detail_html_str = self.parse_url_detail(detail_url)
        detail_html = etree.HTML(detail_html_str)
        # 2. 提取详情页的第一页的图片
        img_url_list = detail_html.xpath("//img[@class='BDE_Image' and not(contains(@ad-dom-img,'true'))]/@src")
        total_img_list.extend(img_url_list)
        # 3.提取下一页的url地址
        detail_next_url = detail_html.xpath("//a[text()='下一页']/@href")
        if len(detail_next_url) > 0:
            detail_next_url = self.add_url + detail_next_url[0]
            print(requests.utils.unquote(detail_next_url))
            return self.get_img_list(detail_next_url, total_img_list)
        return total_img_list  # 返回详情页里面所有图片的url地址列表

    def save_content_list(self, content_list):
        file_path = os.path.abspath(self.tieba_name + ".txt")
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write("\n")

    def save_the_img(self, content_list):
        for content in content_list:
            img_list = content["img_list"]
            img_name = content["title"]
            if img_name == None:
                img_name = "null"
            if len(img_list) > 0:
                for img_url in img_list:
                    response = requests.get(img_url, headers=self.headers2)
                    res = response.content
                    file_path = "pic/{}{}.jpg".format(img_name,
                                                      str(img_list.index(img_url)))
                    # file_path = "pic\{}{}.jpg".format(img_name, str(img_list.index(img_url)))
                    with open(file_path, "wb") as f:
                        f.write(res)

    def run(self):
        current_page = 1
        total_page = 894
        # i=0表示是第一页
        i = 0

        while current_page < total_page:
            # 1.start_url
            # 2.发送请求，获取响应
            # 2.1 提取下一页的url地址
            next_url = self.start_url.format(i * 30)
            print(requests.utils.unquote(next_url))
            html_str = self.parse_url(next_url)
            # print(html_str)
            current_page, total_page = self.get_next_paper(html_str)

            # 3.提取数据
            content_list = self.get_content_list(html_str)
            # 4.保存数据
            self.save_content_list(content_list)
            # 5.保存图片
            self.save_the_img(content_list)
            # 去下一页
            print(i)
            print("爬完%s页了" % current_page)
            print("一共有%s页" % total_page)
            i += 1
            current_page = int(current_page)
            total_page = int(total_page)
            time.sleep(3)


if __name__ == '__main__':
    tieba = TiebaSpider("美女")
    tieba.run()
    # 需要保存的数据 才加上if len(xxx)>0 else None
