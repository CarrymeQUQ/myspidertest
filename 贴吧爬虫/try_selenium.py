# coding=utf-8
from selenium import webdriver
import time
from pprint import pprint


#实例化一个浏览器
# driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver")
driver = webdriver.PhantomJS(executable_path="phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
#设置窗口大小
# driver.set_window_size(1920,1080)

#最大化窗口
driver.maximize_window()

#发送请求
driver.get("http://www.baidu.com")

#进行页面截屏
driver.save_screenshot("./baidu.png")

#元素定位的方法
driver.find_element_by_id("kw").send_keys("python")
driver.find_element_by_id("su").click()

# driver 获取html字符串
# print(driver.page_source) #浏览器中elements的内容

print(driver.current_url)

#driver获取cookie
cookies = driver.get_cookies()
# pprint(cookies)
print("*"*100)
cookies = {i["name"]:i["value"] for i in cookies}
pprint(cookies)
# driver.switch_to.frame()

#退出浏览器
time.sleep(3)
driver.quit()

