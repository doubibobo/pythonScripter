#-*-coding:utf-8-*-
import re 
import urllib2
import os
import sys 
import lxml.html 
import json
#import xlwt
import csv 
#import uniout 
from lxml import etree 
#from bs4 import BeautifulSoup 
import chardet
from pyquery import PyQuery as pq
import HTMLParser
import requests
import gzip, StringIO
import base64
import urllib
sys.path.append('datacenter/')
import datacenter
reload(sys) 
sys.setdefaultencoding( 'utf-8') 

# def download(url,num_retries=2,headers={'User_agent':'wswp'}):
#     print 'Downloading:'+url
#     ##headers={'User_agent':user_agent}
#     headers=headers
#     # headers={
#     #     'referer':'https://www.walmart.com/',
        
#     # }
#     request=urllib2.Request(url,headers=headers)
#     try:
#         html=urllib2.urlopen(request).read()
#     except urllib2.URLError as e:
#         print 'Downloading error:',e.reason
#         html=None
#         if num_retries > 0:
#             if hasattr(e,'code') and 500<=e.code<600:
#                 return download(url,num_retries-1,headers)
#     #print html
#     return html


def download(url,num_retries=2,headers={'User_agent':'wswp'}):
    print 'Downloading:'+url
    headers=headers
    # headers={
    #    'cookie':'ali_apache_id=10.181.239.59.1494788661790.629693.9; ali_beacon_id=10.181.239.59.1494788661790.629693.9; __utma=3375712.567060824.1494788650.1494788798.1494788798.1; __utmc=3375712; __utmz=3375712.1494788798.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=FF6Y4EE1N2-GOQKM0V4V8OX81KS4MMQ3-TP303P2J-SNN; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUxiK7OTLFScnMzizRxdTX0M9J19w%2F09jUIMwmz8I%2BwMPQONvH1DTTWDQkwNjAOMPLSDfbzU9JJLrEyNLE0MbewNLYwMDUz1ElMRhPIrbAyqI0CAE1jHIM%3D; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932765891920%0932659135793; aep_common_f=lloB6SH9JkijCM0tZf5kF3vyLv3h17v3UGN0yKJY3eGouhvEFBCS8A==; cna=7TiaEawi8UUCAdz5Y7Jfecem; acs_usuc_t=acs_rt=9fa376ab0d934f49897582cda74a6a48&x_csrf=1dhm5ajlu9pss; xman_us_t=x_lid=cn1520615299vyjy&sign=y&x_user=sY7/8Mu/TJ74CnXJLTJLG+uzUZKMe5Udm53rpggEULQ=&ctoken=hku5awqv39rt&need_popup=y&l_source=aliexpress; xman_f=r9aP0o7m4kQFmXkQnDDVvHtloUJDl4TJtul01V5pE/TGopjb7kv3ERmNWw/bl4AkL2PUKsbtm0P9uzA1VpN9yTOLXjsCP492Tp0lMn+dZp6lLhPTMTEPlFPB9+Df+xVeZnFC4bm1nRL4VukJ85ff5E6t6GRqQNKTT+rFlACpAt8Xml6pQqUVNwXg2DwEYaUKhuQuJtUCJguhpCa9xCyXT4MffiUY7ExmZH0NG4eesAgpds2lCBCmS6GKkR1JRECrRYDFGYnVYO72CIy4so0cERX0HEVsdrCvu9pBrBOsnUxDLXCvUQWUbfIeT/Pf+rJT49UCdnH0DKQZftBBaUmJL0ZpSZc/5p9+RN8ZPGXplbRkFPIqThB/THcutxz5OKb8K5mSRANDbAR6utSxkYdfPw==; _ga=GA1.2.567060824.1494788650; _gid=GA1.2.511798973.1494791972; _gat=1; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=CN|zheng|quanshi|cnfm|230715779&zero_order=y&last_popup_time=1494791355822; aep_usuc_f=site=glo&region=US&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&x_alimid=230715779&c_tp=USD; intl_locale=en_US; intl_common_forever=y79FmkBQVBQqJv1LtS4vunejUJ855apY0IOmvml/PRSXt6uEoU8RZg==; l=Ajk50FxeJA3yhOmq8aD8iPi8ya4RcS34; isg=AvPzpm8uroKGwmLWP-mLS0CTgvd5y4fq6arxoKWSeJJJpBNGLPgXOlE-KGKx; ali_apache_track=mt=2|ms=|mid=cn1520615299vyjy; ali_apache_tracktmp=W_signed=Y; xman_t=oWB8qjX+m/FChYzepnxuxryFhmGnbqQ023tWzmrFPg31C97Flxcq69qPSvczwM3a+vYgGwjxlyDEUqr1uQKvfSk2yxYTlIXjrfq1qKduCQqLIiofcEw0m34tbPSH0b25clkG0+uN3pj+pI7GcStuSq60x5OEmwFYzxrucHqx+Lw6rdJo6C6cMWZNa98KFo7mVIv9FDorv/rLbURUmXcRtKpzakFP1PQQuM69/LXfW9eltTejIU4ssITXciaL7JBxU0DkVvIdop4ZFwLG9P6TA8CUQb7m3MSFvhW/zdgztKyg7ZgIHUh6+p5FRdLOA3UKSB3+kTw+pQJ4xr1tCTCKBHzTuPCa7RgITEUR7n7LE67o5FtMOy6EZmoZZggReQG5Vo89imAnwnLlsvdjezMswKh87jvo66bJQ423xlN/yUb2n8kO+yeAs/0FeSXltceWR1R50qFg2HO8cEz+QChALI5KC7rzHXLZPSXDt7EzvmoIuKo8UI6Db4Iuefl0t0UhRonofgoh3meoZFidDI2m3ZwfMBTka0hbRoK/fWNvW9FOeQTOzYpBtoFRCd1x1aNmzuF+i6lMvH32E57KJXo/dN4aNF5O6ZDSnMW7hZe75T9pWX1MNIiFmGget/NY3Cx96tgwr7ekv2vseN+4HIo20a5027PyOIoq',
    # }
    request=urllib2.Request(url,headers=headers)
    try:
        response=urllib2.urlopen(request)
        html=urllib2.urlopen(request).read()
        if response.info().get('Content-Encoding')=='gzip':
            html=gzip.GzipFile(fileobj=StringIO.StringIO(html),mode="r")
            try:
                html=html.read()   #.decode('gbk').encode('utf-8')
            except IOError as e1:
                html=urllib2.urlopen(request).read()    #针对 amazon 返回信息 时有错误
    except urllib2.URLError as e:
        print 'Downloading error:',e.reason
        html=None
        if num_retries > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retries-1,headers)
    
    #print html
    return html




def tmall_crawler(html):
    filename='tmall.txt'
    f=open(filename,'w')
    tree=pq(html)
    title=tree('#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-detail-hd > h1').text()
    img=tree('#J_ImgBooth').attr('src')
    desc=tree('#J_AttrUL > li').text().encode('utf-8')
    previous_price=len(tree('#J_StrPriceModBox > dd > span'))
    promote_price=len(tree('#J_PromoPrice > dd > div > span'))  
    f.write(u'标题: '+title+'\n')
    f.write(u'图片: '+'https:'+img+'\n')
    f.write(u'描述: '+desc+'\n')
    f.write(u'原价: '+str(previous_price)+'\n')
    f.write(u'促销价: '+str(promote_price)+'\n')
    f.close()




def taobao_crawler(html,url):
    filename='taobao.txt'
    f=open(filename,'a')
    html=html.decode('GBK')
    tree=pq(html)
    # title=str(tree('#J_Title > h3')).replace('&#160;','')
    # title=pq(title).text().decode('windows-1252').encode('utf-8')
    #print title
    #print chardet.detect(html)
    title=tree('#J_Title > h3').text()#.decode('gb2312').encode('utf-8')#decode('windows-1252','ignore').encode('utf-8')
    print title
    img=tree('#J_ImgBooth').attr('src')
    desc=str(tree('#attributes > ul')).replace('&#160;','')
    desc=pq(desc).text()#.encode('windows-1252')
    # desc=tree('#attributes > ul').text()
    print desc
    #print desc.decode('windows-1252').encode('utf-8')
    previous_price=tree('#J_StrPrice > em.tb-rmb-num').text()
    promote_price=taobao_promoteprice(url)
    
    #print chardet.detect(temp)
    #temp=temp.encode('utf-8').encode('windows-1252')
    # f.write('标题: '.encode('gbk')+title+'\n')
    # f.write(u'图片: '.encode('gbk')+'https:'+img+'\n')
    # f.write(u'描述: '.encode('gbk')+desc+'\n')
    # f.write(u'原价: '.encode('gbk')+str(previous_price)+'\n')
    # f.write(u'促销价: '.encode('gbk')+str(promote_price)+'\n'+'\n'+'\n')
    #update_data(link='',name='',ori_price='',pro_price='',img='',desc='',source='')
    datacenter.update_data(link=url,name=title,img=img,desc=desc,source='taobao',ori_price=previous_price,pro_price=promote_price)
    #f.write(html)
    f.close()

def taobao_promoteprice(url):
    item=url.split('id=')[1].split('&')[0]
    price_url='https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId='+item+'&modules=xmpPromotion'
    req_header = {
        'referer':url   
                 }
    req_timeout = 5
    req = urllib2.Request(price_url,None,req_header)
    resp = urllib2.urlopen(req,None,req_timeout)
    html = resp.read()
    js=json.loads(html)
    return js['data']['promotion']['promoData']['def'][0]['price']
    





def jd_crawler(html):
    
    filename='jd.txt'
    f=open(filename,'w')
    tree=pq(html)
    title=tree('body > div:nth-child(7) > div > div.itemInfo-wrap > div.sku-name').text()
    img=tree('#spec-list > ul > li:nth-child(1) > img').attr('src')
    desc=tree('#detail > div.tab-con > div:nth-child(1) > div.p-parameter > ul.parameter2.p-parameter-list').text().encode('utf-8')
    price_html=tree('#prom-mbuy').attr('data-url')
    print price_html
    price=jd_getprice(price_html)
    print price  
    f.write(u'标题: '+title+'\n')
    f.write(u'图片: '+'https:'+img+'\n')
    f.write(u'描述: '+desc+'\n')
    #f.write(u'原价: '+str(previous_price)+'\n')
    f.write(u'促销价: '+str(price)+'\n')
    f.close()

def jd_getprice(price_html):
    tree=pq(download(price_html))
    price=tree('#jdPrice-copy').text()
    price=price.replace(' ','')
    return price
    



def ama_crawler(html,url):
    # filename='amazon.html'
    # f=open(filename,'w')
    tree=pq(html)
    title=tree('#productTitle').text()
    img=tree('#imgTagWrapperId >img').attr('src')#.encode('utf-8')
    #a-autoid-5-announce > img
    title11=title.replace(' ','')
    
    filename1='static/amazon-pics/'+str(hash(title11))+".jpeg"
    f1=open(filename1,'wb')
    f1.write(base64.b64decode(img.split("base64,")[1]))
    desc=tree('#feature-bullets > ul').text().encode('utf-8')
    price=tree('#priceblock_ourprice ').text()
    
    img_path=filename1
    ori_price=tree('#price').text().split(' ')[1]
    #print price
    # f.write(u'标题: '+title+'\n')
    # f.write(u'图片: '+'https:'+img+'\n')
    # f.write(u'描述: '+desc+'\n')
    # f.write(u'促销价: '+str(price)+'\n')
    datacenter.update_data(link=url,name=title,img=img_path,desc=desc,source='amazon',ori_price=ori_price,pro_price=price)
    # print img
    #f1.close()
    # f.close()




def ebay_crawler(html):
    # filename='ebay.txt'
    # f=open(filename,'a')
    print html
    tree=pq(html)
    title=tree('#itemTitle').text()
    title_delete=tree('#itemTitle >span').text()
    title=title.replace(title_delete,'')
    #print title
    img=tree('#icImg').attr('src')
    #print img
    desc=tree('#vi-desc-maincntr > div.itemAttr > div > table').text().encode('utf-8')
    price=tree('#prcIsum').text()
    datacenter.update_data(link=html,name=title,img=img,desc=desc,source='ebay',ori_price=price,pro_price=price)
    #print price
    # f.write(u'标题: '+title+'\n')
    # f.write(u'图片: '+img+'\n')
    # f.write(u'描述: '+desc+'\n')
    # f.write(u'促销价: '+str(price)+'\n')
    # f.close()





def aliex_crawler(html):
    # filename='aliex.txt'
    # f=open(filename,'a')
    tree=pq(html)
    title=tree('#j-product-detail-bd > div.detail-main > div > h1').text()
    if len(title)==0:
        title=tree('#j-product-detail-bd > div.store-detail-main > div > h1').text()
    #print title
    img=tree('#magnifier > div > a > img').attr('src')
    #print img
    desc=tree('#j-product-desc > div.ui-box.product-property-main > div.ui-box-body > ul').text().encode('utf-8')
    #print desc
    price=tree('#j-product-detail-bd > div.detail-main > div > div.product-price > div > div.p-price-detail.util-clearfix > div > div').text()
    if len(price)==0:
        price=tree('#j-sku-discount-price').text()
    #print price
    # f.write(u'标题: '+title+'\n')
    # f.write(u'图片: '+img+'\n')
    # f.write(u'描述: '+desc+'\n')
    # f.write(u'促销价: '+str(price)+'\n')
    datacenter.update_data(link=html,name=title,img=img,desc=desc,source='aliexpress',ori_price=price,pro_price=price)
    #f.close()



def walmart_crawler(html):
    # filename='walmart.txt'
    # f=open(filename,'a')
    #print html
    tree=pq(html)
    title=tree('body > div.js-content > div > div > div > div.page-content-wrapper.prod-CTA--ada-alt > div > div > div > div.ResponsiveContainer.prod-ProductPage.prod-DefaultLayout.display-flex-ie-compat.direction-flex-column.width-full > div.prod-AboveTheFoldSection.direction-flex-column-m.display-flex-ie-compat > div.prod-leftContainer.display-flex-ie-compat.direction-flex-column > h1 > div').text()
    
    #print title
    img=tree('body > div.js-content > div > div > div > div.page-content-wrapper.prod-CTA--ada-alt > div > div > div > div.ResponsiveContainer.prod-ProductPage.prod-DefaultLayout.display-flex-ie-compat.direction-flex-column.width-full > div.prod-AboveTheFoldSection.direction-flex-column-m.display-flex-ie-compat > div.prod-leftContainer.display-flex-ie-compat.direction-flex-column > div.product-image-carousel-container > div > div > div > div.Grid-col.u-size-1.u-size-10-12-l > div > div > img').attr('src')
    #print img
    desc=tree('body > div.js-content > div > div > div > div.page-content-wrapper.prod-CTA--ada-alt > div > div > div > div.ResponsiveContainer.prod-ProductPage.prod-DefaultLayout.display-flex-ie-compat.direction-flex-column.width-full > div.prod-AboveTheFoldSection.direction-flex-column-m.display-flex-ie-compat > div.prod-leftContainer.display-flex-ie-compat.direction-flex-column > object > div > div > div.ProductPage-short-description-body').text().encode('utf-8')
    #print desc
    pro_price=tree('body > div.js-content > div > div > div > div.page-content-wrapper.prod-CTA--ada-alt > div > div > div > div.ResponsiveContainer.prod-ProductPage.prod-DefaultLayout.display-flex-ie-compat.direction-flex-column.width-full > div.prod-AboveTheFoldSection.direction-flex-column-m.display-flex-ie-compat > div.prod-rightContainer.prod-MarginTop--xs.display-flex-ie-compat.direction-flex-column > div:nth-child(1) > div.prod-Bot.prod-PositionedRelative > div > div.prod-BotRow.prod-showBottomBorder.prod-OfferSection > div > div.prod-ProductOffer.prod-PositionedRelative.Grid.prod-ProductOfferWrapper > div:nth-child(1) > div > span > div > span.hide-content.display-inline-block-m > span > span').text().replace(' ','')
   
    
    datacenter.update_data(link=html,name=title,img=img,desc=desc,source='walmart',ori_price=pro_price,pro_price=pro_price)
    #print ori_price
    # f.write(u'标题: '+title+'\n')
    # f.write(u'图片: '+img+'\n')
    # f.write(u'描述: '+desc+'\n')
    # f.write(u'促销价: '+str(price)+'\n')
    # f.close()

def wish_crawler(url):
    #print url
    cid=url.split('cid=')[1]
    filename='wish.txt'
    f=open(filename,'a')
    #f.write(html)
    headers={'Host':'www.wish.com','X-XSRFToken':'82afda8b0abe4382b0a52df7a43b81f4','Cookie':'_xsrf=82afda8b0abe4382b0a52df7a43b81f4;sweeper_session="Mzk1NGIxZGEtMmJmMS00ODdjLTgxNWItMDM0MTU3YTU2OGQ2MjAxNy0wNS0xNyAxNjoyNzozNi42NDUxOTY=|1495038456|c4f3ff0f5f836df5373ed2bb84d7a2463021a114";'}
    response = requests.post(url='https://www.wish.com/api/product/get', data={'cid':cid},headers=headers)
    response=json.loads(response.text)
    try:
        ori_value=response['data']['contest']['commerce_product_info']['variations'][0]['localized_retail_price']['localized_value']
        img=response['data']['contest']['contest_page_picture']
        pro_value=response['data']['contest']['commerce_product_info']['variations'][0]['localized_price']['localized_value']
        title=response['data']['app_indexing_data']['title'].split('| ')[1]
        desc=response['data']['contest']['description']
        datacenter.update_data(link=url,name=title,img=img,desc=desc,source='wish',ori_price=ori_value,pro_price=pro_value)
        # f.write(u'标题: '+title+'\n')
        # f.write(u'图片: '+img+'\n')
        #f.write(u'描述: '+desc+'\n')
        # f.write(u'原价: '+str(ori_value)+'\n')
        # f.write(u'促销价: '+str(pro_value)+'\n')
    except:
        print '\n'
    f.close()   
def main():
    #headers = {"cookie":'unpl=V2_ZzNtbRAFEBdyDxRTLxpZAGIDRQlLXxcdcl9OB3wdW1VgBBVfclRCFXMUR1FnGlUUZwQZWUdcQhdFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3kcWgVjBBNccmdEJUU4RlBzGVUMVwIiXHIVF0l2CEFcfx4RBmUGFF1GUEIURQl2Vw%3d%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ccb366c6e24441fe89e96f9b656a6663|1493369643290; ipLoc-djd=1-72-2799-0; ipLocation=%u5317%u4EAC; __jda=122270672.234715600.1487761680.1487761680.1493369643.1; __jdb=122270672.6.234715600|1.1493369643; __jdc=122270672; __jdu=234715600; 3AB9D23F7A4B3C9B=UBBL36JY24AFELWRVRDXN4S2NI2HE75KNO3R6YQYRXITJEMNZZB2PBPXKFEXBKH5HE73FMGFDD4BX7RBTTMXSOLGFM'}
#     html=download(headers={'Host':'www.amazon.cn',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
# #'Cookie':'x-wl-uid=1THavC/rD0N6jzORXmNVbENAqfH7SJpwqA93NHIWsGzA+7u1mCzYGnXhco/anZijns/62ohu9WCo=; s_vnum=1926776568027%26vn%3D1; s_nr=1494776568516-New; s_dslv=1494776568517; session-token="hkOObjYk4kRoctM4rpuzBhvLIG2v6F7QfwEJSYykTS/o4L52qCLVMtXxADV04P0rYur3Lb5gaPxTeNsyQJSwYOhDDMhZBFYiF+hSS0m5fAwboaRmQ5Vt4Q7R7vmm47PkpdDlCIzR1/7CiUzwEwBF3bd37SPX5OmrThinIqHerlOzStWBKl8QM8qx6LnHCPUKbWlArP4qVZJ9qX2dEbPyXNOL+FXBgA6ioQwK3QmfojvIrFhnexXhRA=="; csm-hit=1M81JBE6TDGY05RTXVMD+b-N92KYXMME83YVST3KNTH|1496394400276; ubid-acbcn=457-1332951-5893501; session-id-time=2082729601l; session-id=460-1135638-0055835',
# 'Upgrade-Insecure-Requests':'1',
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Encoding':'gzip, deflate, sdch, br',
# 'Accept-Language':'zh-CN,zh;q=0.8',
# 'Cache-Control':'max-age=0',
# 'Connection':'keep-alive'},url='https://www.amazon.cn/U-S-POLO-ASSN-%E7%BE%8E%E5%9B%BD%E9%A9%AC%E7%90%83%E5%8D%8F%E4%BC%9A-%E7%94%B7%E5%BC%8F-%E7%9F%AD%E8%A2%96%E4%BC%91%E9%97%B2%E8%A1%AC%E8%A1%AB-ACSMQ-23601-%E8%93%9D%E7%BA%A2%E6%A0%BC-M/dp/B06XG9WX6B/ref=sr_1_48/459-3806424-9519269?m=A1AJ19PSB66TGU&s=gifts&ie=UTF8&qid=1496400548&sr=1-48&nodeID=%212016157051&psd=1')#('https://www.amazon.cn/dp/B0186FESGW/ref=sa_menu_kindle_l3_ki/460-3702679-0217857')
#     ama_crawler(html,url='')
    
    # url='https://item.taobao.com/item.htm?spm=a1z10.5-c.w4002-16318468846.21.3A2liw&id=549449983832'#'https://item.taobao.com/item.htm?id=544028126656'
    # html=download(url)
    # taobao_crawler(html,url)
    
    # html=download('http://www.ebay.com/itm/WOMENS-FAUX-LEATHER-PATENT-FLATS-DOLLY-BALLET-PUMPS-SWEET-SHOES-UK-SIZE-2-9-/400767756069')
    # ebay_crawler(html)
    
    # html=download('https://www.aliexpress.com/item/Air-Humidifier-Essential-Oil-Diffuser-Aroma-Lamp-Aromatherapy-Electric-Aroma-Diffuser-Mist-Maker-for-Home-Wood/32765891920.html?spm=a2g01.8286187.3.1.38778B&scm=1007.14594.81235.0&pvid=9bc88f84-be49-4c7d-9f4f-3ff44f55bdf4')
    # aliex_crawler(html)

    html=download(headers={'referer':'https://www.walmart.com/'},url='https://www.walmart.com/ip/Stanley-FL5W10-Stanley-Fatmax-Waterproof-LED-Spotlight/21708661?athcpid=21708661&athpgid=athenaHomepage&athcgid=ReviewSummariesItems&athznid=ItemCarouselType_ReviewSummariesItems&athieid=v1&athstid=CS002&athena=true')
    walmart_crawler(html)

    #html=download('https://www.wish.com/#cid=58af9cee033a555281600d42')
    #wish_crawler('https://www.wish.com/#cid=58af9cee033a555281600d42')
if __name__ == '__main__':
    main()