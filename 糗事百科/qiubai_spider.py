import requests
from lxml import etree
import json
import os


class QiubaiSpider:
    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/8hr/page/1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        self.add_url = "https://www.qiushibaike.com"
        self.session = requests.session()
        self.PROXY_POOL_URL = 'http://localhost:5555/random'

    def get_proxy(self):
        try:
            response = requests.get(self.PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def parse_url(self, url):
        proxies = self.get_proxy()
        response = self.session.get(url, headers=self.headers, proxies=proxies)
        html_str = response.content.decode()
        # print(html_str)
        return html_str

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        content_list = []
        div_list = html.xpath("//div[@class='recmd-right']")  # 根据div分组

        for div in div_list:
            item = {}
            item["title"] = div.xpath(".//a[@class='recmd-content']/text()")
            item["title"] = item["title"][0] if len(item["title"]) > 0 else None
            item["title_url"] = div.xpath(".//a[@class='recmd-content']/@href")
            item["title_url"] = self.add_url + item["title_url"][0] if len(item["title_url"]) > 0 else None
            item["username"] = div.xpath(".//a[@class='recmd-user']/span/text()")
            item["username"] = item["username"][0] if len(item["username"]) > 0 else None
            item["userimg_url"] = div.xpath(".//a[@class='recmd-user']/img/@src")
            item["userimg_url"] = "https:" + item["userimg_url"][0].split("?")[0]
            item["good"] = div.xpath(".//div[@class='recmd-num']/span[1]/text()")
            item["good"] = item["good"][0] if len(item["good"]) > 0 else None
            item["comment_num"] = div.xpath(".//div[@class='recmd-num']/span[4]/text()")
            item["comment_num"] = item["comment_num"][0] if len(item["comment_num"]) > 0 else None
            item["comment_list"] = self.get_comment_list(item["title_url"], [])

            content_list.append(item)
        return content_list

    def get_comment_list(self, title_url, comment_list):
        print(title_url)
        start_url = self.add_url + "/commentpage/" + title_url.split("/")[-1] + "?page={}&count=10"
        print(start_url)
        current_page = 1
        while True:
            item = {}
            html_str = self.parse_url(start_url.format(current_page))
            print(html_str)
            html_dict = json.loads(html_str)
            count = html_dict["comments"]["count"]  # 判断是否有下一页
            if count == 0:
                break
            item["page"] = html_dict["comments"]["page"]
            current_page = item["page"]  # 目前是第多少页
            print(current_page)
            # item["total"] = html_dict["comments"]["total"]

            # sum_page = item["total"]//item["count"] + 1  # 一共有多少页
            # print(sum_page)
            item["user_comment"] = []
            items_list = html_dict["comments"]["items"]
            for i in items_list:
                item2 = {}
                item2["login"] = i["login"]
                item2["content"] = i["content"]
                item2["gender"] = i["gender"]
                item2["age"] = i["age"]
                item["user_comment"].append(item2)
            comment_list.append(item)
            current_page += 1

        return comment_list

    def next_url(self, html_str):
        html = etree.HTML(html_str)
        next_url = self.add_url + html.xpath("//span[@class='next']/../@href")[0]
        if next_url == "https://www.qiushibaike.com/hot/":
            print("已经爬完了...程序即将结束...")
            return next_url == None
        return next_url

    def save_content_list(self, content_list):
        file_path = os.path.abspath("糗事百科.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write("\n")

    def run(self):
        next_url = self.start_url
        # start_urlk
        # 发送请求 获取响应
        while next_url is not None:
            print(next_url)
            html_str = self.parse_url(next_url)
            # 提取数据 下一页的数据  标题 标题链接 好笑数 评论数 用户名字 用户头像
            content_list = self.get_content_list(html_str)
            # 保存数据
            self.save_content_list(content_list)
            # 获取下一页url
            next_url = self.next_url(html_str)



if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()
