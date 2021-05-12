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
url_appends = ['tado_heating','tado_air_conditioning','mydlink','whirlpool_washer','whirlpool_dryer','whirlpool_refrigerator','warmup_smart_thermostat',
               '500px','abode','Air_Monitor','aclu','adafruit','AduroSmart','agile_octopus','aisync','air_by_propeller','IQAir',
               'airtable','airthings','alko_smart_garden','amazon_alexa','ambiclimate','ambient_weather','apa','android_battery',
               'android_device','android_phone','android_photos','android_messages','angelcam','AnywareServices','apilio','appkettle','app_store',
               'aquanta','aquarea_smart_cloud','arlo','LDSArnoo_eu','asana','asusrouter','asuszeneye','attm2x','augusthome','aura','awair',
               'ballotpedia','bart_delay','bbox_miami','bdrthermeagroup','beam','beeminder','bernafon','beseye','best_buy','BG_HOME',
               'bhome','bitly','blink','blink_eu','blogger','bloomsky','bluebyadt','blueconnect','blueair_aware','blueair_classic_i',
               'bouncie','boxoh','brainyquote','brilliant_smart','broadlink','Bucky','buffer','bea','do_button','caavo','caleo','caltrain','do_camera',
               'camio','cdc','cta','City_of_Edmonton','tampa','clicksend','clinicaltrials','link_smart_home',
               'cloudrain','ComEd_HourlyPricing','comed_pts','coqon','cortana','dlink_connected_home_camera','dlink_motion_sensor',
               'dlink_water_sensor','dlink_wifi_router','daikin_online_controller','dailymotion','danalock','dart','daskeyboardq',
               'date_and_time','deezer','delicious','usda','dod','dol','dos','diigo','docsend','dominos','domovea','donation_manager',
               'dondeesta','dropbox','easycontrol_bosch','ecobee','eight','eff','email',
               'energenie_mi_home','eia','epa','envoy','era','evernote','everykit','ewelink','ezviz','facebook','facebook_pages','fansync',
               'fcc','feedly','fibaro','filtrete','finance','fitbit','fiverr','flic','flickr','flo','followupcc','foobot','fcu_tod','foursquare','foxnews',
               'fujitsu_general_limited','futurehome','garadget','garageio','garagewifi','ge_appliances_cooking','ge_appliances_dishwasher','ge_appliances_dryer',
               'ge_appliances_geospring','ge_appliances_refrigerator','ge_appliances_washer','ge_appliances_wac','genius_hub',
               'gideon','giphy','gira','github','go','google_assistant','google_calendar','google_contacts','google_docs','google_drive','google_sheets',
               'google_wifi','grants','greenwavesystems','griddy','grouplotse','gumroad','hacker_news','hager_iot','harvest','heatmiser',
               'hella_onyx','legrand_home_control','hc_coffee_machine','hc_cook_processor','hc_hob','hc_dishwasher','hc_dryer',
               'hc_fridge','hc_hood','hc_oven','hc_cleaning_robot','hc_washer','home8','homecontrol_flex','homeseer','homey',
               'honeywell_lyric','hubitat','automower','idevices','ifttt','ihaus_smoke_detector','ihomecontrol','ihome_enhance','inoreader',
               'instagram','instapaper','instyle','intelligent_home','imf','intesishome','invoxia_tracker','invoxia_triby','ios_calendar','ios_contacts',
               'ios_photos','ios_reminders','iot_podcast','iottysmarthome','irobot','isitchristmas','isecurityplus','ismartalarm','ispy_agent','ivideon',
               'i_zone','jotform','kaiterra','king_county_metro','knocki','kronaby','kyber','lametric','leeo','lennoxicomfort','vesyncIftttAirPurifier',
               'lg_dryer','lg_smartphone','lg_washer','loc','liebherr','life360','lightwaverf_heating','lightwaverf_lighting','lightwaverf_power',
               'LinkMyPet','linkdesk','LinkJapan_eHome','whisker','littlebits','location','lockitron','logitech_circle','logitech_pop','longreads',
               'maestro_by_stelpro','Magic_Home','mailchimp','manything','mdsha','mcamviewz','medium','meistertask','meross',
               'mesh','migo','misfit','kumocloud','miyo','moniai','monzo','moodo','muilab','musaic','musixmatch','my_leviton',
               'mydlink','myfox_homecontrol','mymilan','myq_devices','mystrom','myuplink','naacp','narrative','narro','nsf','nvd','nature',
               'nefit_easy','nest_cam','nest_protect','nest_thermostat','netatmo_security','netatmo_thermostat','netatmo','netro','neurio',
               'newsblur','nexia','nexx','nibe_uplink','nice','nikohomecontrol','nj_transit','nomos_system','noonhome','safetrek','do_note',
               'notion','npr','nuki_opener','nuki','nVent_Nuheat','oco_camera','office_365_calendar','office_365_contacts','office_365_mail',
               'ohmconnect','onedrive','ooma','openhab','orion','orro','oticon','particle','pebblebee','pert','pew_research',
               'hearlink','phone_call','phyn','pinboard','pinterest','pocket','viva','product_hunt','propublica','pryv','electrolux',
               'putio','qapital','qnap','qualitytime','quip','rachio_iro','raindrop','rain_machine',
               'Ratoc_remocon','reddit','rememberthemilk','remotelync','rescuetime','ring','feed','SAFEBYHUB6',
               'salesforce','samsungairpurifier','samsungairconditioner','SamsungRefrigerator','SamsungRobotVacuum','SamsungRoomAirconditioner',
               'SamsungWasher','sateraito_office','scoutalarm','sec','sengled','sense_energy_monitor','sesame',
               'sfgate','sfmta','sharpr','sighthound','simcam','simplehuman','sina_weibo','skybell','skylinknet','skyroam','slashdot','smanos','smappee',
               'smart_home_solution','smartlife','smarter','oge','smartthings','somfy_thermostat',
               'somfy_protect','songkick','sonic','sothebys','soundcloud','space','sparnord','sports_illustrated','spotcam','spotify','square','sRemo','ssgsmart',
               'stacklighting','stockimo','strava','stripe','surveymonkey','swannsecurity','switchbot','tado_hot_water','tado_air_conditioning','tado_heating',
               'tailwind','teamsnap','tecan','tecan_connect','telegram','telldus','weatherflow','tesco','texas_legislature','nytimes','thermosmart',
               'thinga','tantiv4','time','tivo','tmt_chow','todoist','tomtom_satnav','toodledo','ttc','resideo_total_connect','tplink_router','trello',
               'True_Energy','tumblr','turntouch','twitch','twitter','us_independence_day','uber','ubibot','uhoo',
               'unodc','uplinkremote','uscert','usagov','verizon_cloud',
               'vesyncBulb','vesyncDimmer','vesync','vesyncSwitchOnline','vimeo','vaillant','warmup_smart_thermostat','watts',
               'weather','cisco_spark','maker_webhooks','weebly','wemo_airpurifier','wemo_coffeemaker','wemo_dimmer','wemo_humidifier',
               'wemo_insight_switch','wemo_light_switch','wemo_lighting','wemo_maker','wemo_motion','wemo_slowcooker','wemo_switch',
               'whirlpool_dryer','whirlpool_refrigerator','whirlpool_washer','whistle','wifiplug','wikipedia','relay','eggminder','porkfolio',
               'spotter','wirelesstag','withings','withingshome','WithingsSleep','woopla','wordpress','workflow',
               'who','wwf','wyzecam','yolink','youtube','zware','zeeq','zubie']
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
