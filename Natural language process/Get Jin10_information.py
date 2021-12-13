# coding=UTF-8
from jieba import cut
from requests import get
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from ssl import _create_unverified_context
from time import time,sleep,mktime
from json import loads
from csv import writer,reader
from os.path import exists
from sys import exc_info
from datetime import datetime
from pytz import timezone
from random import normalvariate
filename='text_analysis.csv'
def record_to_csv(information,f_name=filename):
    '''
    将每次记录的新闻保存在text-analysis中
    '''
    with open(f_name,'a',newline='') as myfile:
        csvwriter=writer(myfile)
        csvwriter.writerow(information)
def utc_2_pk(utctime_str:str,format='%Y-%m-%dT%H:%M:%S.%fZ')->datetime:
    '''UTC时间字符串转化为北京时间的datetime对象
    :参数 utctime_str:UTC时间字符串，格式为yyyy-m-d H
    '''
    # 构造出没有时区的datetime对象
    naive_time = datetime.strptime(utctime_str,format)
    # 取出上述对象的年月日小时构造一个时区为utc的datetime对象
    utctime = datetime(naive_time.year,naive_time.month,naive_time.day,naive_time.hour,naive_time.minute,tzinfo=timezone('UTC'))

    # 把时区为utc的对象转化为时区为Asia/Shanghai的datetime对象
    pktime =utctime.astimezone(timezone('Asia/Shanghai'))
    return pktime

def get_news(unix_time):
    context = _create_unverified_context()
    print("Now unix_time",unix_time)
    req = Request(url="https://www.jin10.com/flash_newest.js?" + str(unix_time))
    html = urlopen(req, context=context).read()
    # dsObj=BeautifulSoup(html.read())
    # 去掉原来javascript中变量定义的语句
    loads_result = str(html, encoding='utf-8')[14:-2]
    # 重新使用Json语法定义
    loads_result = '{"newest_news":[' + loads_result
    loads_result = loads_result + ']}'
    # 调用json库的loads解析
    loads_result = loads(loads_result)
    last_news_time=None
    #判断文本数据文件是否存在，存在的话在前面已储存数据的基础上新增记录。
    if exists(filename)==True:

        with open(filename, 'r') as read_file:
            reading = list(reader(read_file))
            '''展示现有已经储存的信息
            for i in reading:
                print(i)
            '''
            print("现有信息记录")
            #读取上次记录的最新新闻记录
            last_news_time = mktime(utc_2_pk(reading[-1][0][:19],format='%Y-%m-%d %H:%M:%S').timetuple())
    counts = 0
    for i in range(len(loads_result['newest_news'])-1,0,-1):
        news_time = mktime(utc_2_pk(loads_result['newest_news'][i]['time']).timetuple())
        if last_news_time==None:
            record_to_csv([
            utc_2_pk(loads_result['newest_news'][i]['time']),
            loads_result['newest_news'][i]['type'],
            #如果是文字内容，则直接读取content内容，否则使用字符串操作符讲数据重新组合成文本语句
            loads_result['newest_news'][i]['data']['content'] if 'content' in loads_result['newest_news'][i]['data'].keys() else loads_result['newest_news'][i]['data']['country']+loads_result['newest_news'][i]['data']['name']+loads_result['newest_news'][i]['data']['name']+loads_result['newest_news'][i]['data']['actual']+','+loads_result['newest_news'][i]['data']['previous'],
            loads_result['newest_news'][i]['important'],
            loads_result['newest_news'][i]['channel'],
            loads_result['newest_news'][i]['remark']
        ])
        else:
            print(news_time,last_news_time)
            if news_time<=last_news_time:
                print("已经有相关记录")
            else:
                record_to_csv([
                    utc_2_pk(loads_result['newest_news'][i]['time']),
                    loads_result['newest_news'][i]['type'],
                    # 如果是文字内容，则直接读取content内容，否则使用字符串操作符讲数据重新组合成文本语句
                    loads_result['newest_news'][i]['data']['content'] if 'content' in loads_result['newest_news'][i]['data'].keys() else loads_result['newest_news'][i]['data']['country'] + loads_result['newest_news'][i]['data'][
                        'name'] + loads_result['newest_news'][i]['data']['name'] + loads_result['newest_news'][i]['data']['actual'] + ',' + loads_result['newest_news'][i]['data']['previous'],
                    loads_result['newest_news'][i]['important'],
                    loads_result['newest_news'][i]['channel'],
                    loads_result['newest_news'][i]['remark']
                ])
                counts+=1
    print("更新%d条，更新率%f"%(counts,float(counts)/len(loads_result['newest_news'])))
'''
获取当前时间
'''
while 1<10:
    try:
        get_news(time())
    # 控制频率,防止被目标网站ban掉
        print("Updated One")
        sleep(abs(normalvariate(10 * 60, 5)))
    except:
        print(exc_info())

