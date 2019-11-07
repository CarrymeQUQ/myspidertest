import json
import time
import pdfkit

import requests

base_url = 'https://mp.weixin.qq.com/mp/profile_ext'



# 这些信息不能抄我的，要用你自己的才有效
headers = {
    'Connection': 'keep-alive',
    'Accept': '* / *',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1278.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU2ODYzNTkwMg==&scene=124&uin=MTg5NzM1MDUxOQ%3D%3D&key=5b405373aa09951da414f0cf7049c75688764f8df4e4f7f9bb9a5ada9402ebc6c9c8c72846916a6b3190aff5a7b4f708f94faf0b943d853808caa87605b51f25a6ff5349ef831a07d14c54b4d936bf7c&devicetype=Windows+10&version=62070152&lang=zh_CN&a8scene=7&pass_ticket=AoZO4Ms50yjQyj1mpkL3xUbjTMGLKqSaBcm4ioKsMdOB%2BVi1gnIM2O52fpoXM0zi&winzoom=1',
    'Accept-Encoding': 'gzip, deflate',
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {
    'devicetype': 'iPhoneiOS13.1.2',
    'lang': 'zh_CN',
    # 
    'pass_ticket': 'AoZO4Ms50yjQyj1mpkL3xUbjTMGLKqSaBcm4ioKsMdOBVi1gnIM2O52fpoXM0zi',
    'version': '17000829',
    # 
    'wap_sid2': 'CPeK3YgHElxnZlJ0NzRnMFVnY2gySW51akhJLUxtWmo1SkprY1RRMXEzNXExTmUwQzNrc21PQzBESFBQR3JnVDNPTGV3bTZpMi1ZQ3k2aDV6V1ZwVUdRUkZKTTBLd29FQUFBfjCon47uBTgNQJVO',
    'wxuin': '1897350519'
}


def get_params(offset):
    params = {
        'action': 'getmsg',
        # 
        '__biz': 'MzU2ODYzNTkwMg==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '124',
        'uin': 'MTg5NzM1MDUxOQ==',
        # 1
        'key': '8d3f7565c056ebe6e3457e606b021921d912c7e46b9ce6c226b7aa53f16a2d6d58e71aa8d1bc642762bca0daddc2918e889fb64e81603ab82b2193477dd6d1b50dd9576426c3ba66eb0cae968011b583',
        'pass_ticket': 'AoZO4Ms50yjQyj1mpkL3xUbjTMGLKqSaBcm4ioKsMdOB+Vi1gnIM2O52fpoXM0zi',
        # 2
        'appmsg_token': '1034_zH41gtUczSmic%2BgB2BYk9_zqLnWfOblC3NTpGw~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_list_data(offset):
    res = requests.get(base_url, headers=headers, params=get_params(offset), cookies=cookies)
    data = json.loads(res.text)
    print(res.url)
    # print(data)
    # 状态信息
    ret = data["ret"]
    status = data["errmsg"] 
    # print(ret,status)
    can_msg_continue = data['can_msg_continue']
    next_offset = data['next_offset']
    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']

    for data in list_data:
        try:
            if ret == 0 or status == 'ok':         
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                # print(title)
                content_url = msg_info['content_url']
                # print(content_url)
                # 自己定义存储路径
                pdfkit.from_url(content_url, "{}.pdf".format(title))
                # pdfkit.from_string(html, "{}.pdf".format(title))
                print('获取到原创文章：%s ： %s' % (title, content_url))
            else:
                print('Before break , Current offset is %d' % next_offset)
                break
        except:
            print('不是图文')

    if can_msg_continue == 1:
        time.sleep(1)
        print('next offset is %d' % next_offset)
        get_list_data(next_offset)


if __name__ == '__main__':
    get_list_data(0)