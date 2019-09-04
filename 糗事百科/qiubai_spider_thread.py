import requests
from lxml import etree
import json
import os
import threading
from queue import Queue


class QiubaiSpider:
    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/8hr/page/1"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        self.add_url = "https://www.qiushibaike.com"
        self.session = requests.session()
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()
        self.title_url_queue = Queue()
        self.comment_list_queue = Queue()

    def parse_url(self):
        self.url_queue.put(self.start_url)
        while True:
            url = self.url_queue.get()
            response = self.session.get(url, headers=self.headers)
            html_str = response.content.decode()
            # print(html_str)
            # return html_str
            self.html_queue.put(html_str)
            # -1
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            print(html)
            next_url = self.add_url + html.xpath("//span[@class='next']/../@href")[0]
            print("***" * 20 + next_url)
            if next_url == "https://www.qiushibaike.com/hot/":
                print("已经爬完了...程序即将结束...")
                # next_url = None
            self.url_queue.put(next_url)
            content_list = []
            # content_list2 = []
            content_list.append({"next_url":next_url})

            div_list = html.xpath("//div[@class='recmd-right']")  # 根据div分组

            for div in div_list:
                item = {}
                item["title"] = div.xpath(".//a[@class='recmd-content']/text()")
                item["title"] = item["title"][0] if len(item["title"]) >0 else None
                item["title_url"] = div.xpath(".//a[@class='recmd-content']/@href")
                item["title_url"] = self.add_url + item["title_url"][0] if len(item["title_url"]) >0 else None
                item["username"] = div.xpath(".//a[@class='recmd-user']/span/text()")
                item["username"] = item["username"][0] if len(item["username"]) > 0 else None
                item["userimg_url"] = div.xpath(".//a[@class='recmd-user']/img/@src")
                item["userimg_url"] = "https:" + item["userimg_url"][0].split("?")[0]
                item["good"] = div.xpath(".//div[@class='recmd-num']/span[1]/text()")
                item["good"] = item["good"][0] if len(item["good"]) >0 else None
                item["comment_num"] = div.xpath(".//div[@class='recmd-num']/span[4]/text()")
                item["comment_num"] = item["comment_num"][0] if len(item["comment_num"])>0 else None
                self.title_url_queue.put(item["title_url"])
                item["comment_list"] = self.comment_list_queue.get()
                content_list.append(item)
                # content_list.append(content_list2)
                self.comment_list_queue.task_done()


            # return content_list
            self.content_queue.put(content_list)
            # -1
            self.html_queue.task_done()

    def get_comment_list(self):
        while True:
            title_url = self.title_url_queue.get()
            print(title_url)
            start_url = self.add_url + "/commentpage/" + title_url.split("/")[-1] + "?page={}&count=10"

            current_page = 1
            comment_list = []
            while True:
                item = {}
                print(start_url.format(current_page))
                html_str = requests.get(start_url.format(current_page), headers=self.headers).content.decode()
                # print(html_str)

                html_dict = json.loads(html_str)
                count = html_dict["comments"]["count"]  # 判断是否有下一页
                if count == 0:
                    break
                item["page"] = html_dict["comments"]["page"]
                current_page = item["page"]  # 目前是第多少页
                # print(current_page)
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

            self.comment_list_queue.put(comment_list)
            self.title_url_queue.task_done()


    # def get_url_list(self):
    #     self.url_queue.put(self.start_url)
    #     next_url = self.start_url
    #     while next_url is not None:
    #         html_str = self.html_queue.get()
    #         # print(html_str)
    #         html = etree.HTML(html_str)
    #         next_url = self.add_url + html.xpath("//span[@class='next']/../@href")[0]
    #         print(next_url)
    #         if next_url == "https://www.qiushibaike.com/hot/":
    #             print("已经爬完了...程序即将结束...")
    #             next_url = None
    #         self.url_queue.put(next_url)
    #         print(self.url_queue)
            # self.html_queue.task_done()

    def save_content_list(self):
        while True:
            # print(self.content_queue)
            content_list = self.content_queue.get()
            # print(content_list)
            file_path = os.path.abspath("糗事百科2.txt")
            with open(file_path, "a", encoding="utf-8") as f:
                for content in content_list:
                    f.write(json.dumps(content, ensure_ascii=False, indent=4))
                    f.write("\n")
            print("保存成功")
            self.content_queue.task_done()

    def run(self):
        thread_list = []
        # start_urlk
        # 发送请求 获取响应

        t_parse = threading.Thread(target=self.parse_url)
        thread_list.append(t_parse)
        # 提取数据 下一页的数据  标题 标题链接 好笑数 评论数 用户名字 用户头像

        t_content = threading.Thread(target=self.get_content_list)
        thread_list.append(t_content)
        for i in range(2):
            t_comment = threading.Thread(target=self.get_comment_list)
            thread_list.append(t_comment)
        # 保存数据
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)
        print("开始")
        print(thread_list)
        for t in thread_list:
            t.setDaemon(True)   # 把子线程设置为守护线程 该线程是不重要的 主程序一旦结束 子线程立马结束
            t.start()

        for q in [self.url_queue,self.html_queue,self.content_queue,self.title_url_queue,self.comment_list_queue]:
            q.join()    # 让主线程等待堵塞 等待队列中的任务完成后才完成
        print("主线程结束.................")


if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()

