import requests
import re
from bs4 import BeautifulSoup

# 发送url请求得到其文本信息，设定时间为30s
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r
    except:
        return ""

theHTML = getHTMLText("http://www.baidu.com")

print(BeautifulSoup(theHTML.content))
