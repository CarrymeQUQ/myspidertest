# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from project2.items import Project2Item
import re
import pymysql
from pymongo import MongoClient

client = MongoClient()


class Project2Pipeline(object):
    def open_spider(self, spider):
        # 连接mysql
        self.client = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='mysql',
            database='suning',
            charset='utf8'
        )
        self.cur = self.client.cursor()
        # 链接mongodb
        # self.collection = client[spider.settings.get("DB")][spider.settings.get("COLLECTION")]

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Project2Item):
            item["book_author"] = self.process_content(item["book_author"])
            item["book_publish"] = self.process_content(item["book_publish"])
            print(item)
            # self.collection.insert(dict(item))

            # 大分类　小分类　小分类地址　
            m_cate = item["m_cate"]
            s_cate = item["s_cate"]
            s_href = item["s_href"]
            # 图书地址　图书名字　图书封面　作者　出版社　出版日期
            book_href = item["book_href"]
            book_name = item["book_name"]
            book_img_url = item["book_img_url"]
            book_author = item["book_author"]
            book_publish = item["book_publish"]
            book_date = item["book_date"]
            # book_price = item["b_cate"]

            list = [m_cate, s_cate, s_href, book_href, book_name,
                    book_img_url, book_author, book_publish, book_date]

            sql = "insert into books(m_cate, s_cate, s_href, book_href, book_name, book_img_url, book_author, book_publish, book_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql, list)
            self.client.commit()
            # 获取查询的结果
            #result = self.cur.fetchone()
            # result = self.cur.fetchall()
            # 打印查询的结果
            # print(result)
        return item

    def process_content(self, content):
        if content is not None:
            content = re.sub(r"\s", "", content)
            # 去除字符串中的空字符串
        return content
