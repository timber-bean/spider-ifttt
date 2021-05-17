#-*-coding:utf-8-*-
#---------------------
#author:
#   timber
#data:
#   2021.05.07
#description:
#   spider in IFTTT
#---------------------

from selenium import webdriver
from lxml import etree
import json
import jsonpath
import pymongo
from urllib.parse import urlencode
import time


#连接数据库
client = pymongo.MongoClient(host='localhost',port=27017)
db = client.test
collection = db.rules


#从文件中读取html的后缀
def get_suffix(file_name):
    buffer = []
    try:
        file = open(file_name, "r")
        #读取文件内容
        for id in file.readlines():
            buffer.append(id)
        file.close()
    except IOError:
        print("Can't find file!")
    return buffer

if __name__ == '__main__':

    #源网址
    base_url = 'https://ifttt.com'

    #存储网页后缀的文件
    file_name = "continue.txt"

    #网址的后缀
    url_appends = get_suffix(file_name)

    #启动模拟浏览器
    browser = webdriver.Chrome()

    #对于每个后缀，都构成一个url
    for url_append in url_appends:
        url = base_url + url_append

        #获取网页源代码
        browser.get(url)
        page_source = browser.page_source
        print(url_append)
        time.sleep(15) #需要等一段时间，使其渲染完成
        
        #page_source.text 为响应体的内容，即真正的网页源码
        html = etree.HTML(page_source)

        #使用 xpath 选择属性，获取需要的内容
        result = html.xpath('//div[@data-react-class="App.Comps.ConnectionCard.SettingsButton"]/@data-react-props')
        if(result == []):
            print("Fail!")
            continue
        #把json形式的字符串转换成python形式的Unicode字符串
        page_json = json.loads(result[0])
        
        #解析json
        applet = jsonpath.jsonpath(page_json,"$.connection")[0]
              
        if len(applet['permissions'])>1:
            dict = {'id':' ','Name':' ','author':'','Trigger_service':'','Trigger_name':' ','Trigger_description':' ','Action_service':'','Action_name':'','Action_description':'','Shares':0}
            dict['id'] = applet['id']
            dict['Name'] = applet['name']
            dict['author'] = applet['author']
            dict['Trigger_service'] = applet['permissions'][0]['service_name']
            dict['Trigger_name'] = applet['permissions'][0]['name']
            dict['Trigger_description'] = applet['permissions'][0]['description']
            dict['Action_service'] = applet['permissions'][1]['service_name']
            dict['Action_name'] = applet['permissions'][1]['name']
            dict['Action_description'] = applet['permissions'][1]['description']
            dict['Shares'] = applet['installs_count']
            collection.insert_one(dict) #插入MongoDB中

        print("finish!")
        #等待20秒再进行下一次爬取
        time.sleep(20)

    #一个脚本只能打开一个webdriver，因此最后关闭
    browser.close()
