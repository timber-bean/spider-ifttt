#-*-coding:utf-8-*-
#---------------------
#author:
#   timber
#data:
#   2021.04.20
#description:
#   get common applet id from IFTTT
#---------------------

from selenium import webdriver
from lxml import etree
from urllib.parse import urlencode
import time
import re

#从文件中读取html的后缀
def get_suffix(file_name):
    buffer = []
    try:
        file = open(file_name, "r")
        #读取文件内容
        buffer = file.readlines()[0].split(",")
        file.close()
    except IOError:
        print("Can't find file!")
    return buffer

#写入文件
def write_file(app_id):
    file_name = "applet_id.txt"
    try:
        file = open(file_name, "a+")
        file.write(app_id)
        file.write("\n")
        file.close()
    except IOError:
        print("Can't find file!")


if __name__ == '__main__':
    
    #源网址
    base_url = 'https://ifttt.com/'
    
    #存储网页后缀的文件
    file_name = "common.txt"

    #网址的后缀
    url_appends = get_suffix(file_name)

    #启动模拟浏览器
    browser = webdriver.Chrome()


    #对于每个后缀，都构成一个url
    for url_append in url_appends:
        url = base_url + url_append
        
        #获取网页信息
        browser.get(url)
        print(url_append)
        time.sleep(15) #需要等一段时间，使其渲染完成
        
        #page_source 为网页源码
        page_source = browser.page_source
        html = etree.HTML(page_source)

        #使用 xpath 选择属性，获取每个规则的链接
        applet_ids = []
        applet_ids = html.xpath('//li[@class="my-web-applet-card web-applet-card"]/a/@href')

        ids_length = len(applet_ids)
        for i in range(ids_length):
            #转换为字符串
            applet_id = str(applet_ids[i])
            #匹配非applet的链接，如果不是，则不写入文件
            if(re.match('/connect/',applet_id) == None):
                write_file(applet_id)
        
        #等待5秒再进行下一次爬取
        time.sleep(10)
        
    #一个脚本只能打开一个webdriver，因此最后关闭
    browser.close()
