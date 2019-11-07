from urllib.parse import urlencode
import requests, pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
# 调用键盘按键操作时需要引入的Keys包
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import json

# 连接数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='mysql',
                             db='weibo',
                             charset='utf8')

cursor = connection.cursor()
sql = "USE weibo;"
cursor.execute(sql)
connection.commit()


def create_sheet(bozhu):
    try:
        weibo = '''
            CREATE TABLE {}(
                ID  VARCHAR (255) NOT NULL PRIMARY KEY,
                text VARCHAR (255),
                attitudes VARCHAR (255),
                comments VARCHAR (255), 
                reposts VARCHAR (255) 
            )
        '''.format(bozhu)
        # 序号 INT  NOT NULL PRIMARY KEY AUTO_INCREMENT,
        cursor.execute(weibo)
        connection.commit()
    except:
        pass


def url_get():
    browser = webdriver.Chrome("../贴吧爬虫/chromedriver_linux64/chromedriver")
    browser.maximize_window()
    browser.get(url='https://m.weibo.cn/')
    sleep(3)
    browser.find_element_by_class_name("m-text-cut").click()
    sleep(3)
    bozhu_id = input('输入博主ID：')
    create_sheet(bozhu_id)
    browser.find_element_by_tag_name("input").send_keys(bozhu_id)
    sleep(3)
    # 模拟Enter回车键
    browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)
    sleep(3)
    search = browser.find_element_by_class_name('m-img-box')
    search.click()
    sleep(3)
    # bz_num = browser.find_element_by_class_name('name_txt')
    # bz_num.click()
    # sleep(5)
    # 开启了一个新页面，需要跳转到新页面
    # handles = browser.window_handles
    # browser.switch_to_window(handles[1])
    print(browser.current_url)
    # cookies = browser.get_cookies()
    # print(cookies)
    return browser.current_url,bozhu_id

# https://m.weibo.cn/u/2145291155?uid=2145291155&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%A9%AC%E4%BA%91
# https://m.weibo.cn/api/container/getIndex?type=uid&value=2145291155&containerid=1076032145291155
# 拼接url 1076032145291155
def get_page(page,value,containerid):
    base_url = "https://m.weibo.cn/api/container/getIndex?"
    headers = {
    'Host': 'm.weibo.cn',
    # 'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }
    # 查询字符串
    params = {
        'type': 'uid',
        'value': value,
        'containerid': containerid,
        'page': page
    }
    # 调用urlencode() 方法将params参数转化为 URL 的 GET请求参数
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        # print(type(response.content.decode()))
        response_dict = json.loads(response.content.decode())
        status = response_dict["ok"]
        if response.status_code == 200 and status == 1:
            # print(response.json())
            return response.json(),status
        else:
            return 0,0
            
    except requests.ConnectionError as e:
        print('Error', e.args)


# 存储数据，存储到数据库
def parse_page(all_data,bozhu_id):
    if all_data:
        items = all_data.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog')
                # weibo = {}
                # weibo['id'] = item.get('id')
                # weibo['text'] =
                # weibo['attitudes'] = item.get('attitudes_count')
                # weibo['comments'] = item.get('comments_count')
                # weibo['reposts'] = item.get('reposts_count')
                weibo = []
                weibo.append(item.get('id'))
                weibo.append(pq(item.get('text')).text())
                weibo.append(item.get('attitudes_count'))
                weibo.append(item.get('comments_count'))
                weibo.append(item.get('reposts_count'))
                # print(weibo)
                # 遇见重复数据，pass，是根据主键来判断，如果是重复数据，忽略，但是报警告
                try:
                    sql = '''INSERT INTO {}(ID,text,attitudes,comments,reposts)
                          VALUES (%s,%s,%s,%s,%s) '''.format(bozhu_id)
                    cursor.execute(sql, weibo)
                    connection.commit()
                except:
                    pass
            yield weibo

def get_containerid(value):
    base_url = "https://m.weibo.cn/api/container/getIndex?"
    headers = {
    'Host': 'm.weibo.cn',
    # 'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }
    # 查询字符串
    params = {
        'type': 'uid',
        'value': value,
    }
    # 调用urlencode() 方法将params参数转化为 URL 的 GET请求参数
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.content.decode())
        status = response_dict["ok"]
        if response.status_code == 200 and status == 1:
            containerid = response_dict["data"]["tabsInfo"]["tabs"][1]["containerid"]
            return containerid
    except requests.ConnectionError as e:
        print('Error', e.args)


if __name__ == '__main__':
    current_url_str,bozhu_id = url_get()
    # https://m.weibo.cn/u/2145291155?uid=2145291155&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%A9%AC%E4%BA%91
    # currentPage = int(re.findall("param.currentPage = \"(.*?)\";", response.body.decode())[0])
    value = re.findall("uid=(\d+?)&",current_url_str)[0]
    print(value)
    containerid = get_containerid(value)
    print(containerid)
    page = 1
    while True:
        all_data,status = get_page(page,value,containerid)
        print(status)
        if status == 0:
            print("爬完了")
            break
        results = parse_page(all_data,bozhu_id)
        for result in results:
            print(result)
        print("当前爬取到%s页!!!" % page)
        page += 1

cursor.close()

# 可以爬任意指定博主所有微博，以博主名建立表，分别储存信息
# 使用selenium+PhantomJS抓取对应博主主页链接