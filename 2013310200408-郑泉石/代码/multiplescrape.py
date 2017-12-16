#-*-coding:utf-8-*-
from pyquery import PyQuery as pq
import sys 
import urllib2
import singlescrape
import threading
import chardet
import gzip, StringIO
import time
import requests
import json
from urllib import unquote
import chardet
import brotli
reload(sys) 
sys.setdefaultencoding( 'utf-8') 


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
        #print response.info().get('Content-Encoding')
        if response.info().get('Content-Encoding')=='gzip':
            #print 'shit'
            html=gzip.GzipFile(fileobj=StringIO.StringIO(html),mode="r")
            try:
                html=html.read()          #.decode('gbk').encode('utf-8')
            except IOError as e1:
                html=urllib2.urlopen(request).read()    #针对 amazon 返回信息 时有错误
        if response.info().get('Content-Encoding')=='br':
            html=brotli.decompress(html)
    except urllib2.URLError as e:
        print 'Downloading error:',e.reason
        html=None
        if num_retries > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,num_retries-1,headers)
    
    #print html
    return html


def taobao_multi(url):
    html=download(url)
    shop_name=url.split('//')[1].split('.taobao')[0]
    path=url.split('.com')[1].split('?')[0]
    taobao_crawler(html,shop_name,path)


def taobao_crawler(html,shop_name,path):
    filename='taobao_sort.txt'
    f=open(filename,'w')
    tree=pq(html)
    wid=tree("#bd .col-main div div").attr('data-widgetid')#("div[data-title='宝贝列表']").attr('data-widgetid')#("#shop16318468846").attr('data-widgetid')
    print wid
   
    item_urls='https://'+shop_name+'.taobao.com/i/asynSearch.htm?'+'mid='+'w-'+wid+'-0'+'&'+'path='+path
    data_html=download(item_urls)
    taobao_items_crawler(data_html,f)
    #print item_urls
    f.close()

def taobao_items_crawler(data_html,f):
    #f.write(data_html)
    tree=pq(data_html)
    items=tree("dd a").items()
    imgs=tree("dt a img").items()
    
    print "item_href:"
    for item in items:
        if '&' not in item.attr('href'):
            print 'https:'+item.attr('href').split('\"')[1].split('\\')[0]
            t=threading.Thread(target=singlescrape.taobao_crawler,args=(download('https:'+item.attr('href').split('\"')[1].split('\\')[0]),'https:'+item.attr('href').split('\"')[1].split('\\')[0],))
            t.start()
    # print "img_href:"
    # for img in imgs:
    #     print 'https:'+img.attr('src').split('\"')[1].split('\\')[0]
    









def ebay_multi(url):       
    html=download(url)
    #print html
    #print html
    filename='ebay_sort.txt'
    f=open(filename,'w')
    f.write(html)
    tree=pq(html)
    items=tree("#result-set  >.item-cell")#.attr('href')#("div[data-title='宝贝列表']").attr('data-widgetid')#("#shop16318468846").attr('data-widgetid')
    
    for item in items.items():
        
        t=threading.Thread(target=singlescrape.ebay_crawler,args=(pq(item)('.desc >a').attr('href'),))
        t.start()
    
    #print item_urls
    f.close()     
    if tree('#pager > a.gspr.nextBtn').attr('href') != None:
        ebay_multi(tree('#pager > a.gspr.nextBtn').attr('href')  )




def amazon_multi(url,headers={'Host':'www.amazon.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
#'Cookie':'x-wl-uid=1THavC/rD0N6jzORXmNVbENAqfH7SJpwqA93NHIWsGzA+7u1mCzYGnXhco/anZijns/62ohu9WCo=; s_vnum=1926776568027%26vn%3D1; s_nr=1494776568516-New; s_dslv=1494776568517; session-token="hkOObjYk4kRoctM4rpuzBhvLIG2v6F7QfwEJSYykTS/o4L52qCLVMtXxADV04P0rYur3Lb5gaPxTeNsyQJSwYOhDDMhZBFYiF+hSS0m5fAwboaRmQ5Vt4Q7R7vmm47PkpdDlCIzR1/7CiUzwEwBF3bd37SPX5OmrThinIqHerlOzStWBKl8QM8qx6LnHCPUKbWlArP4qVZJ9qX2dEbPyXNOL+FXBgA6ioQwK3QmfojvIrFhnexXhRA=="; csm-hit=1M81JBE6TDGY05RTXVMD+b-N92KYXMME83YVST3KNTH|1496394400276; ubid-acbcn=457-1332951-5893501; session-id-time=2082729601l; session-id=460-1135638-0055835',
'Upgrade-Insecure-Requests':'1',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive'}):
    headers=headers
    html=download(url,headers=headers)
    print chardet.detect(html)
    f=open('shitama.html','w')
    f.write(html)
    tree=pq(html)

    items=tree(".s-result-list-atf >li")
    retry=0
    while len(items)==0 and retry<5:
        headers=headers
        html=download(url,headers=headers)
        tree=pq(html)
        items=tree(".s-result-list >li")
        retry+=1
    for item in items.items():
       
        item_url=pq(item)('a').attr('href')
        print item_url
       
        t=threading.Thread(target=singlescrape.ama_crawler,args=(download(url=item_url,headers={'Host':'www.amazon.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
#'Cookie':'x-wl-uid=1THavC/rD0N6jzORXmNVbENAqfH7SJpwqA93NHIWsGzA+7u1mCzYGnXhco/anZijns/62ohu9WCo=; s_vnum=1926776568027%26vn%3D1; s_nr=1494776568516-New; s_dslv=1494776568517; session-token="hkOObjYk4kRoctM4rpuzBhvLIG2v6F7QfwEJSYykTS/o4L52qCLVMtXxADV04P0rYur3Lb5gaPxTeNsyQJSwYOhDDMhZBFYiF+hSS0m5fAwboaRmQ5Vt4Q7R7vmm47PkpdDlCIzR1/7CiUzwEwBF3bd37SPX5OmrThinIqHerlOzStWBKl8QM8qx6LnHCPUKbWlArP4qVZJ9qX2dEbPyXNOL+FXBgA6ioQwK3QmfojvIrFhnexXhRA=="; csm-hit=1M81JBE6TDGY05RTXVMD+b-N92KYXMME83YVST3KNTH|1496394400276; ubid-acbcn=457-1332951-5893501; session-id-time=2082729601l; session-id=460-1135638-0055835',
'Upgrade-Insecure-Requests':'1',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive'}),item_url,))
        t.start()
        #     i+=1
    
    # #print item_urls
    #f.close()     
    # if tree('#pagnNextLink').attr('href') != None:
    #     ebay_multi(tree('#pagnNextLink').attr('href')  )


def aliex_multi(url):    #目前必须带cookie爬
    html=download(url=url,headers={'cookie':'ali_apache_id=10.181.239.59.1494788661790.629693.9; ali_beacon_id=10.181.239.59.1494788661790.629693.9; __utma=3375712.567060824.1494788650.1494788798.1494788798.1; __utmc=3375712; __utmz=3375712.1494788798.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=FF6Y4EE1N2-GOQKM0V4V8OX81KS4MMQ3-TP303P2J-SNN; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUxiK7OTLFScnMzizRxdTX0M9J19w%2F09jUIMwmz8I%2BwMPQONvH1DTTWDQkwNjAOMPLSDfbzU9JJLrEyNLE0MbewNLYwMDUz1ElMRhPIrbAyqI0CAE1jHIM%3D; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932765891920%0932659135793; aep_common_f=lloB6SH9JkijCM0tZf5kF3vyLv3h17v3UGN0yKJY3eGouhvEFBCS8A==; cna=7TiaEawi8UUCAdz5Y7Jfecem; acs_usuc_t=acs_rt=9fa376ab0d934f49897582cda74a6a48&x_csrf=1dhm5ajlu9pss; xman_us_t=x_lid=cn1520615299vyjy&sign=y&x_user=sY7/8Mu/TJ74CnXJLTJLG+uzUZKMe5Udm53rpggEULQ=&ctoken=hku5awqv39rt&need_popup=y&l_source=aliexpress; xman_f=r9aP0o7m4kQFmXkQnDDVvHtloUJDl4TJtul01V5pE/TGopjb7kv3ERmNWw/bl4AkL2PUKsbtm0P9uzA1VpN9yTOLXjsCP492Tp0lMn+dZp6lLhPTMTEPlFPB9+Df+xVeZnFC4bm1nRL4VukJ85ff5E6t6GRqQNKTT+rFlACpAt8Xml6pQqUVNwXg2DwEYaUKhuQuJtUCJguhpCa9xCyXT4MffiUY7ExmZH0NG4eesAgpds2lCBCmS6GKkR1JRECrRYDFGYnVYO72CIy4so0cERX0HEVsdrCvu9pBrBOsnUxDLXCvUQWUbfIeT/Pf+rJT49UCdnH0DKQZftBBaUmJL0ZpSZc/5p9+RN8ZPGXplbRkFPIqThB/THcutxz5OKb8K5mSRANDbAR6utSxkYdfPw==; _ga=GA1.2.567060824.1494788650; _gid=GA1.2.511798973.1494791972; _gat=1; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=CN|zheng|quanshi|cnfm|230715779&zero_order=y&last_popup_time=1494791355822; aep_usuc_f=site=glo&region=US&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&x_alimid=230715779&c_tp=USD; intl_locale=en_US; intl_common_forever=y79FmkBQVBQqJv1LtS4vunejUJ855apY0IOmvml/PRSXt6uEoU8RZg==; l=Ajk50FxeJA3yhOmq8aD8iPi8ya4RcS34; isg=AvPzpm8uroKGwmLWP-mLS0CTgvd5y4fq6arxoKWSeJJJpBNGLPgXOlE-KGKx; ali_apache_track=mt=2|ms=|mid=cn1520615299vyjy; ali_apache_tracktmp=W_signed=Y; xman_t=oWB8qjX+m/FChYzepnxuxryFhmGnbqQ023tWzmrFPg31C97Flxcq69qPSvczwM3a+vYgGwjxlyDEUqr1uQKvfSk2yxYTlIXjrfq1qKduCQqLIiofcEw0m34tbPSH0b25clkG0+uN3pj+pI7GcStuSq60x5OEmwFYzxrucHqx+Lw6rdJo6C6cMWZNa98KFo7mVIv9FDorv/rLbURUmXcRtKpzakFP1PQQuM69/LXfW9eltTejIU4ssITXciaL7JBxU0DkVvIdop4ZFwLG9P6TA8CUQb7m3MSFvhW/zdgztKyg7ZgIHUh6+p5FRdLOA3UKSB3+kTw+pQJ4xr1tCTCKBHzTuPCa7RgITEUR7n7LE67o5FtMOy6EZmoZZggReQG5Vo89imAnwnLlsvdjezMswKh87jvo66bJQ423xlN/yUb2n8kO+yeAs/0FeSXltceWR1R50qFg2HO8cEz+QChALI5KC7rzHXLZPSXDt7EzvmoIuKo8UI6Db4Iuefl0t0UhRonofgoh3meoZFidDI2m3ZwfMBTka0hbRoK/fWNvW9FOeQTOzYpBtoFRCd1x1aNmzuF+i6lMvH32E57KJXo/dN4aNF5O6ZDSnMW7hZe75T9pWX1MNIiFmGget/NY3Cx96tgwr7ekv2vseN+4HIo20a5027PyOIoq',})
    tree=pq(html)
    items=tree("#node-gallery > div.module.m-o.m-o-large-all-detail > div > div > ul > li h3")
    for item in items.items():
        #print 'https:'+pq(item)('a').attr('href')
        t=threading.Thread(target=singlescrape.aliex_crawler,args=('https:'+pq(item)('a').attr('href'),))
        t.start()
    # #f.close()     
    if tree('#pagination-bottom > div.ui-pagination-navi.util-left > a.ui-pagination-next').attr('href') != None:
        aliex_multi('https:'+tree('#pagination-bottom > div.ui-pagination-navi.util-left > a.ui-pagination-next').attr('href')  ) 

def walmart_multi(url,now_page):
    html=download(url=url,headers={'referer':'https://www.walmart.com/'})
    tree=pq(html)
    items=tree("#searchProductResult > ul > li > div > div.search-result-product-title.gridview > a")
    for item in items.items():
        t=threading.Thread(target=singlescrape.walmart_crawler,args=('https://www.walmart.com'+pq(item).attr('href'),))
        t.start()
    lastpage=0 
    
    for page in tree('#centerContent > div:nth-child(4) > div.paginator > ul > li > button').items():
        #print pq(page).text()
        if int(pq(page).text())>lastpage:
            lastpage=int(pq(page).text())

    if now_page+1<lastpage:
        now_page+=1
        walmart_multi(url.split('?')[0]+'?offset='+str(40*now_page),now_page ) 
def wish_multi(url):
    query=url.split('merchant/')[1].split('#default')[0]
    #print unquote(query).encode('utf-8')
    count=40
    start=70
    # filename='wish_sort.txt'
    # f=open(filename,'w')
    while start<1000:
        print start
        headers={'Host':'www.wish.com','X-XSRFToken':'82afda8b0abe4382b0a52df7a43b81f4','Cookie':'_xsrf=82afda8b0abe4382b0a52df7a43b81f4;sweeper_session=Mzk1NGIxZGEtMmJmMS00ODdjLTgxNWItMDM0MTU3YTU2OGQ2MjAxNy0wNS0xNyAxNjoyNzozNi42NDUxOTY=|1495038456|c4f3ff0f5f836df5373ed2bb84d7a2463021a114'}
        response = requests.post(url='https://www.wish.com/api/merchant', data={'query':unquote(query),'count':count,'start':start},headers=headers)
        #print response.text
        response=json.loads(response.text)
        try:
            for item in response['data']['results']:
                t=threading.Thread(target=singlescrape.wish_crawler,args=('cid='+item['commerce_product_info']['id'],))
                t.start()  
        except:
            print '\n'       
        
        start+=count

    
def main():
    now_page=0
    #url='https://uneedbra.taobao.com/category-1215303808.htm?spm=a1z10.5-c-s.w4002-13942925140.91.XlUpl2&_ksTS=1494343036792_266&callback=jsonp267&mid=w-13942925140-0&wid=13942925140&path=%2Fcategory-1215303808.htm&search=y&catName=%D1%A5%D7%D3&catId=1215303808&pageNo=1#anchor'
    #url='https://shop493672783.taobao.com/category-1292854523.htm?spm=a1z10.1-c.w5002-16318468833.6.6zJkQf&search=y&catName=%D2%C2%CE%EF%CF%B4%BB%A4'
    url='http://stores.ebay.com/austenmayfair/Sweaters-/_i.html?_fsub=1721998011'
    ebay_multi(url)
    #taobao_multi(url)
    # url='https://www.amazon.cn/s/ref=s9_acss_bw_cg_Apparel_2a1_w?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&rh=i%3Aapparel%2Cn%3A2016156051%2Cn%3A%212016157051%2Cn%3A2152155051%2Cn%3A51869071%2Cp_6%3AA1AJ19PSB66TGU%2Cn%3A!2016157051&bbn=51869071&sort=date-desc-rank&rw_html_to_wsrp=1&pf_rd_m=A1U5RCOVU0NYF2&pf_rd_s=merchandised-search-10&pf_rd_r=X3CRQYD271ANXN5MH8YE&pf_rd_t=101&pf_rd_p=0a7952fb-d8f7-4b60-80cd-429dd7ea332e&pf_rd_i=2016156051'
    # amazon_multi(url)
    # url='https://kbaybo.aliexpress.com/store/group/Humidifier/1396009_506929092/1.html?spm=2114.12010612.0.0.0b7da7&origin=n&SortType=bestmatch_sort&g=y'
    # aliex_multi(url)
    # url='https://www.walmart.com/c/brand/castrol-motor-oil'
    # walmart_multi(url,now_page)
    #wish_multi('https://www.wish.com/merchant/%E6%9D%AD%E5%B7%9E%E9%85%B7%E4%BB%91%E6%9C%8D%E9%A5%B0%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8')
    
if __name__ == '__main__':
    main()