#-*-coding:utf-8-*-
#---------------------
#author:
#   timber
#data:
#   2020.05.26
#description:
#   spider in IFTTT
#---------------------

import requests
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


#源网址
base_url = 'https://ifttt.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

#网址的后缀
#url_appends = ['alko_smart_garden','asusrouter','asuszeneye','Air_Monitor','AduroSmart','air_by_propeller','airtouch','airthings','amazon_alexa','ambiclimate','ambient_weather','android_battery','android_device','AnywareServices','aquanta','arlo','LDSArnoo_eu','augusthome','automatic_pro','awair','bhome','blink_eu','bluebyadt','blueair_classic_i','bouncie','brilliant_smart','caavo','link_smart_home','dlink_connected_home_camera','dlink_motion_sensor','dlink_wifi_router','danalock','eight','energenie_mi_home','futurehome','garadget','garagewifi','garageio','gideon','gira','griddy','google_wifi','hager_iot','heatmiser','hc_oven','hc_dishwasher','hc_washer','hc_dryer','hc_coffee_machine','hc_hood','hc_hob','hc_fridge','home8','homeseer','homey','honeywell_lyric','ivideon','vesyncIftttAirPurifier','life360','lightwaverf_heating','lightwaverf_lighting','lightwaverf_power','LinkJapan_eHome','my_leviton','nest_cam','nikohomecontrol','noonhome','SamsungWasher','SamsungRefrigerator','SamsungRobotVacuum','SamsungRoomAirconditioner','samsungairpurifier','skylinknet','smartlife','smart_home_solution','smartthings','wemo_lighting','wemo_motion','wemo_light_switch','wemo_insight_switch','wemo_dimmer','wemo_maker','wemo_coffeemaker','wemo_slowcooker','wemo_airpurifier','wemo_humidifier','withingshome','WithingsSleep','ihome_enhance','ihomecontrol','tado_hot_water','tado_heating','tado_air_conditioning','mydlink','whirlpool_washer','whirlpool_dryer','whirlpool_refrigerator','warmup_smart_thermostat']
url_appends = ['tado_heating','tado_air_conditioning','mydlink','whirlpool_washer','whirlpool_dryer','whirlpool_refrigerator','warmup_smart_thermostat']
#url_appends = ['alko_smart_garden','asusrouter','asuszeneye','Air_Monitor','AduroSmart','air_by_propeller','airtouch','airthings','amazon_alexa','ambiclimate','ambient_weather','android_battery','android_device','AnywareServices','aquanta','arlo','LDSArnoo_eu','augusthome','automatic_pro','automatic_pro','awair','bhome','blink_eu','bluebyadt','blueair_classic_i','bouncie','brilliant_smart','caavo','link_smart_home','dlink_connected_home_camera','dlink_motion_sensor','dlink_wifi_router','danalock','eight','energenie_mi_home','futurehome','garadget','garagewifi','garageio','gideon','gira','griddy','google_wifi','hager_iot','heatmiser','hc_oven','hc_dishwasher','hc_washer','hc_dryer','hc_coffee_machine','hc_hood','hc_hob','hc_fridge','home8','homeseer','homey','honeywell_lyric','ivideon','vesyncIftttAirPurifier','life360','lightwaverf_heating','lightwaverf_lighting','lightwaverf_power','LinkJapan_eHome','my_leviton','nest_cam','nikohomecontrol','noonhome','SamsungWasher','SamsungRefrigerator','SamsungRobotVacuum','SamsungRoomAirconditioner','samsungairpurifier','skylinknet','smartlife','smart_home_solution','smartthings','wemo_lighting','wemo_motion','wemo_light_switch','wemo_insight_switch','wemo_dimmer','wemo_maker','wemo_coffeemaker','wemo_slowcooker','wemo_airpurifier','wemo_humidifier','withingshome','WithingsSleep','ihome_enhance','ihomecontrol','tado_hot_water',]

for url_append in url_appends:
    url = base_url + url_append

    #获取网页源代码
    page_source = requests.get(url, headers = headers)

    if page_source.status_code == 200:
        #page_source.text 为响应体的内容，即真正的网页源码
        html = etree.HTML(page_source.text)

        #使用 xpath 选择属性，获取需要的内容
        result = html.xpath('//div[@data-react-class="App.Comps.DiscoverServiceView"]/@data-react-props')
        application = html.xpath('//div[@class="brand-section"]/a/@title')
        #print(result[0])


        #把json形式的字符串转换成python形式的Unicode字符串
        page_json = json.loads(result[0])

        #python形式的列表
        applets_list = jsonpath.jsonpath(page_json,"$.applets[*]")


        for applet in applets_list:
            if len(applet['permissions'])>1:
                dict = {'id':' ','application':'','Name':' ','Trigger_name':' ','Trigger_description':' ','Action_name':'','Action_description':'','Shares':0}
                dict['id'] = applet['id']
                dict['application'] = application[0]
                dict['Name'] = applet['name']
                dict['Trigger_name'] = applet['permissions'][0]['name']
                dict['Trigger_description'] = applet['permissions'][0]['description']
                dict['Action_name'] = applet['permissions'][1]['name']
                dict['Action_description'] = applet['permissions'][1]['description']
                dict['Shares'] = applet['installs_count']
                collection.insert_one(dict) #插入MongoDB中
                #print(dict)
        time.sleep(10)
    else:
        print(application[0])
        print(page_source.status_code)
        time.sleep(120)
        print('\n')
