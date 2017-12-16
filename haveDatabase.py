import re
from databaseConfig import *
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# MongoDB配置信息
client = pymongo.MongoClient(MONGO_URL)
database = client[MONGO_DB]

# 打开Chrome浏览器
profileDir = "C:Users\\zhuch\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\l1hp9srt.default"
profile = webdriver.FirefoxProfile(profileDir)


chromeBrower = webdriver.Firefox(profile)
wait = WebDriverWait(chromeBrower, 10)

# 第一次搜索页面的方法
def search():
    print("正在搜索")
    try:
        chromeBrower.get("https://www.taobao.com")
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()

# 运用selenium进行翻页的操作
def next_page(page_number):
    print("正在翻页")
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

# 运用pyquery进行页面的解析
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = chromeBrower.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        products = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(products)
        save_to_monogo(products)

# 将数据保存到monogo中
def save_to_monogo(result):
    try:
        if database[MONGO_TABLE].insert(result):
            print("存储成功！", result)
    except Exception:
        print("存储失败", result)

# 主方法
def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print("下载中断，遥远的外星球")
    finally:
        chromeBrower.close()

if __name__ == '__main__':
    main()