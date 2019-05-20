# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Queue
import  threading


import codecs

from time import sleep
import logging
logging.basicConfig(level = logging.DEBUG)

count_value = 1234  #每类景点爬取个数

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/201002201 Firefox/55.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
csvfile = open('lvyouData.csv','w',encoding='utf-8', newline='')

writer = csv.writer(csvfile)
writer.writerow(["区域","名称","类别","景点id","主题","级别","热度","地址","特色","价格","人气排名"])

def download_page(url):  # 下载页面,没用到
    try:
        data = requests.get(url, headers=HEADERS, allow_redirects=True).content  # 请求页面，获取要爬取的页面内容
        return data
    except:
        pass

#下载页面 如果没法下载就 等待1秒 再下载
def download_soup_waitting(url):
    try:
        sleep(random.random())
        response= requests.get(url,headers=HEADERS,allow_redirects=False,timeout=5)
        if response.status_code==200:
            html=response.content
            html=html.decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            return soup
        else:
            sleep(1)
            print("等待ing")
            return download_soup_waitting(url)
    except:
        return ""

def getTypes():
    types=["文化古迹","自然风光","展馆","公园","农家度假","游乐场","城市观光","运动健身"] 
    for type in types:
        url="http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest&sort=pp&subject="+type+"&page=1"
        getType(type,url,0)



def getType(type,url,count):
    soup=download_soup_waitting(url)
    search_list=soup.find('div', attrs={'id': 'search-list'})
    sight_items=search_list.findAll('div', attrs={'class': 'sight_item'})
    # print("search_list: %s ", search_list)
    # print("sight_items: %s ", sight_items)
    for sight_item in sight_items:
        
        count = count + 1
        
        if count > count_value:
            break
        theme=type
        data_id = sight_item['data-id']
        name=sight_item['data-sight-name']
        category = sight_item['data-sight-category']
        districts=sight_item['data-districts']
        address=sight_item['data-address']
        level=sight_item.find('span',attrs={'class':'level'})
        if level:
            level=level.text
        else:
            level=""
        product_star_level=sight_item.find('span',attrs={'class':'product_star_level'})
        if product_star_level:
            product_star_level=product_star_level.text
        else:
            product_star_level=""
        intro=sight_item.find('div',attrs={'class':'intro'})
        if intro:
            intro=intro['title']
        else:
            intro=""
        price=sight_item.find('span',attrs={'class':'sight_item_price'})
        if price:
            price=price.text
        else:
            price=""
            
        # print("level:" , level)
        # print("intro:" , intro)
        # print("price:" , price)
        print("")
        print(count , [districts.replace("\n",""),name.replace("\n",""),category.replace("\n",""),data_id.replace("\n",""),theme.replace("\n",""),level.replace("\n",""),product_star_level.replace("\n",""),address.replace("\n",""),intro.replace("\n",""),price])

        writer.writerow([districts.replace("\n",""),name.replace("\n",""),category.replace("\n",""),data_id.replace("\n",""),theme.replace("\n",""),level.replace("\n",""),product_star_level.replace("\n",""),address.replace("\n",""),intro.replace("\n",""),price,count])
    next=soup.find('a',attrs={'class':'next'})
    
    if count < count_value:
        if next:
            next_url="http://piao.qunar.com"+next['href']
            getType(type,next_url,count)
 
 
 
if __name__ == '__main__':
    getTypes()