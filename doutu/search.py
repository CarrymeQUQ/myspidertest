import glob
import time
import random
import itchat
from itchat.content import TEXT, PICTURE
import requests

imgs = []


def searchImage(text):
    print('收到关键词: ', text)
    for name in glob.glob('/home/python/桌面/spider/myspidertest/doutu/images/biaoqingbao/*' + text + '*.jpg'):
        imgs.append(name)
    for name in glob.glob('/home/python/桌面/spider/myspidertest/doutu/images/biaoqingbao/*' + text + '*.gif'):
        imgs.append(name)


@itchat.msg_register([PICTURE, TEXT])
def text_reply(msg):
    searchImage(msg.text)
    # room = itchat.search_friends(name='Hola')
    # print(room)
    # userName = room[0]['UserName']
    # print(room[0])
    # print(userName)
    print("备注:", msg.user['RemarkName'])
    print("微信名:", msg.user['NickName'])
    print(msg.user['UserName'])
    # if msg.user['UserName'] == userName:
    for img in imgs[:6]:
        # for x in range(0,6):
        #     img = random.choice(imgs)
        # itchat.send_image(img, toUserName=userName)
        msg.user.send_image(img)
        time.sleep(0.3)
        print('开始发送表情： ', img)
    imgs.clear()


itchat.auto_login(hotReload=True)
itchat.run()
