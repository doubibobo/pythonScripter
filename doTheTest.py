import requests
from bs4 import BeautifulSoup
import re

# 发送url请求得到其文本信息，设定时间为30s
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 获取商品的信息
def parserPage(goodsList, html):
    title = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
    plt = re.findall(r'\"raw_title\"\:\".*?\"', html)
    print(title)
    print(plt)
    for i in range(len(title)):
        theTitle = eval(title[i].split(':')[1])
        price = eval(plt[i].split(':')[1])
        goodsList.append([theTitle, price])

# 打印页面
def printPage(goodList):
    tplt = "{:6}\t{:8}\t{:16}"
    file = open("taobao.txt", "w")
    file.write(tplt.format("序号", "价格", "商品名称"))
    for i in range(len(goodList)):
        goods = goodList[i]
        file.write(tplt.format(i+1, goods[0], goods[1]))

# 启动函数
def begin():
    goods = "固态硬盘"
    depth = 1
    url = "https://s.taobao.com/search?q="
    goodList = []
    for i in range(depth):
        print(url+goods+"&s"+str(i*44))
        html = getHTMLText(url+goods+"&s"+str(i*44))
        print(html)
        parserPage(goodList, html)
    printPage(goodList)

begin()