from selenium import webdriver
import time
import json
import requests
from pprint import pprint
from pymongo import MongoClient


class DouyuSpider:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome("../贴吧爬虫/chromedriver_linux64/chromedriver")
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}
        self.seesions = requests.session()
        client = MongoClient(host="localhost", port=27017)
        self.collection = client["douyu"]["douyupspider"]

    def get_content_list(self):
        # target = self.driver.find_element_by_xpath("//div[@class='ListFooter']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

        for i in range(14):
            self.driver.execute_script('window.scrollBy(0, {}00)'.format(i))
            time.sleep(2)

        li_list = self.driver.find_elements_by_xpath("//div[contains(@class,'layout-Module-container') and contains(@class,'layout-Cover')]/ul[@class='layout-Cover-list']/li")
        content_list = []

        for li in li_list:
            item = {}
            item["room_img(房间封面)"] = li.find_element_by_xpath(".//div[@class='DyListCover-imgWrap']//img[1]").get_attribute(
                "src").split("/webpdy1")[0]
            # item["room_img"] = li.find_element_by_xpath(".//img[@class='DyImg-content is-normal ']").get_attribute(
            #     "src").split("/webpdy1")[0]
            item["room_title(房间标题)"] = li.find_element_by_xpath(".//h3[@class='DyListCover-intro']").get_attribute("title")
                # text
            item["room_cate(房间分类)"] = li.find_element_by_xpath(".//span[@class='DyListCover-zone']").text
            item["anchor_name(主播ID)"] = li.find_element_by_xpath(".//h2[@class='DyListCover-user']").text
            item["watch_num(主播热度)"] = li.find_element_by_xpath(".//span[@class='DyListCover-hot']").text
            # pprint(item)
            content_list.append(item)
        # 获取下一页的元素
        next_url = self.driver.find_elements_by_xpath("//li[@class=' dy-Pagination-next']")
        # next_url = self.driver.find_elements_by_xpath("//li[@aria-disabled='false']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        file_path = ("douyu.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write("\n")
        print("内容保存成功")
        for content in content_list:
            img_path = ("images/{}.jpg").format(content["anchor_name(主播ID)"])
            img_url = content["room_img(房间封面)"]
            img = self.seesions.get(img_url, headers=self.headers).content
            with open(img_path, "wb") as f:
                f.write(img)
        print("房间封面保存成功")

    def save_to_mongodb(self, content_list):
        print(content_list)
        self.collection.insert_many(content_list)
        print("保存到数据库成功")
        # for i in t.inserted_ids:
        #     print(i)


    def run(self):
        # 最大化窗口
        self.driver.maximize_window()
        # self.driver.set_window_size(1000, 30000)
        # 1.start_url
        # 2.发送请求 获取响应
        self.driver.get(self.start_url)
        time.sleep(1)
        # 3.提取数据 提取下一页的元素
        content_list, next_url = self.get_content_list()
        # 4.保存数据
        self.save_content_list(content_list)
        # 保存数据到数据库
        self.save_to_mongodb(content_list)
        # 5.点击下一页的元素 循环
        while next_url is not None:
            next_url.click()
            time.sleep(1)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)
            self.save_to_mongodb(content_list)


if __name__ == '__main__':
    douyuspider = DouyuSpider()
    douyuspider.run()
