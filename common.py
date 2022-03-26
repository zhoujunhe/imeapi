import base64
import re
from urllib.request import urlopen
from urllib.parse import quote

'''
获取文件二进制buff   
参数为 img   如果是url,直接通过urlopen下载图片流，如果是base64编码，直接解码成二进制图片流
'''
def getFileBuff(img):
    # 使用正则匹配url,如果不是url 读取base64编码内容
    if re.match(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", img):
        buff = urlopen(quote(img, safe='/:?=&')).read()
    else:
        str_base64 = img[img.find(",") + 1:]
        buff = base64.b64decode(str_base64)
    return buff

