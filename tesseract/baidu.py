from aip import AipOcr

from PIL import Image

""" 你的 APPID AK SK """

APP_ID = '17538772'

API_KEY = 'x6c1f6bspWzT0ACjhYxqMgjL'

SECRET_KEY = 'NAoL9AxNMXMfVyWpYe1EX8BP4CGRHcGV'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 先将图像进行处理

image = Image.open('20181229205022579.png')


# 灰度处理

image = image.convert('L')
image.show()
# 二值化处理 默认127

# image = image.convert('1')

# def convert_img(img, threshold):
#     img = img.convert("L")  # 处理灰度
#     pixels = img.load()
#     for x in range(img.width):
#         for y in range(img.height):
#             if pixels[x, y] > threshold:
#                 pixels[x, y] = 255
#             else:
#                 pixels[x, y] = 0
#     return img
#
#
# image = convert_img(image, 110)
# image.show()

image.save('baidu.jpg')

image = get_file_content('baidu.jpg')

# """ 调用通用文字识别, 图片参数为本地图片 """

result = client.basicGeneral(image)

print(result)

# """ 如果有可选参数 """

# options = {}

# options["language_type"] = "ENG"

# options["detect_direction"] = "true"

# options["detect_language"] = "true"

# options["probability"] = "true"

# """ 带参数调用通用文字识别（高精度版） """

# result = client.basicGeneral(image, options)

# print(result)


for word in result['words_result']:
    print(word['words'])
