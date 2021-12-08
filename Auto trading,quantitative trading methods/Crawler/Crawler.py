import requests as rs
import json as js
import pandas
import time
import knoema
import pandas as pd
import urllib
import random
defined_interval='1d'
choiced_timepoint=int(time.time())
proxy={
    'https':'49.74.22.224:8118',
    'https':'60.188.19.44:3000'
}
dict_choiced_timelenth={
    '1m':60*60*24,
    '2m':60*60*24*2,
    '5m':60*60*24*5,
    '15m':60*60*24*15,
    '60m':60*60*24*30,
    '1d':60*60*24*365,
    '1w':60*60*24*365*3
}
dict_choiced_timerange={
    '1m':'1d',
    '2m':'1d',
    '5m':60*60*24*5,
    '15m':60*60*24*15,
    '60m':60*60*24*30,
    '1d':60*60*24*365,
    '1w':60*60*24*365*3
}
dict_normal_list_yahoo={
'YM=F':['道琼斯指数期货','DOW Futures'],
                     'ES=F':['标准普尔500期货','S&P Futures'],
                     'NQ=F':['纳斯达克指数期货','Nasdaq Futures'],
                     'RTY=F':['罗素2000指数期货','Russell 2000 Futures'],
                 'CL=F':['道琼斯指数期货','DOW Futures'],
                 'GC=F':['道琼斯指数期货','DOW Futures'],
                 '^TNX':['道琼斯指数期货','DOW Futures'],
                 '^VIX':['道琼斯指数期货','DOW Futures'],
                 '^FTSE':['道琼斯指数期货','DOW Futures']
}
dict_worldindics_yahoo={'^GSPC':'S&P 500',
                  '^DJI':'Dow Jones Industrial Average',
                  '^IXIC':'NASDAQ Composite',
                  '^NYA':'NYSE COMPOSITE (DJ)',
                  '^XAX':'NYSE AMEX COMPOSITE INDEX',
                  '^BUK100P':'Cboe UK 100 Price Return',
                  '^RUT':'Russell 2000',
                  '^VIX':'Vix',
                  '^FTSE':'FTSE 100',
                  '^GDAXI':'DAX PERFORMANCE-INDEX',
                  '^FCHI':'CAC 40',
                  '^STOXX50E':'ESTX 50 PR.EUR',
                  '^N100':'EURONEXT 100',
                  '^BFX':'BEL 20',
                  'IMOEX.ME':'MOEX Russia Index',
                  '^N225':'Nikkei 225',
                  '^HSI':'HANG SENG INDEX',
                  '000001.SS':'SSE Composite Index',
                  '^STI':'STI Index',
                  '^AXJO':'S&P/ASX 200',
                  '^AORD':'ALL ORDINARIES',
                  '^BSESN':'S&P BSE SENSEX',
                  '^JKSE':'Jakarta Composite Index',
                  '^KLSE':'FTSE Bursa Malaysia KLCI',
                  '^NZ50':'S&P/NZX 50 INDEX GROSS',
                  '^KS11':'KOSPI Composite Index',
                  '^TWII':'TSEC weighted index',
                  '^GSPTSE':'S&P/TSX Composite index',
                  '^BVSP':'IBOVESPA',
                  '^MXX':'IPC MEXICO',
                  '^IPSA':'S&P/CLX IPSA',
                  '^MERV':'MERVAL',
                  '^TA125.TA':'TA-125',
                  '^CASE30':'EGX 30 Price Return Index',
                  '^JN0U.JO':'Top 40 USD Net TRI Index'
}
dict_futures_yahoo={
    'ES=F':'S&P Futures',
    'YM=F':'Dow Futures',
    'NQ=F':'Nasdaq Futures',
    'RTY=F':'Russell 2000 Futures',
    'ZB=F':'U.S. Treasury Bond Futures,Jun-',
    'ZN=F':'10-Year T-Note Futures,Jun-2020',
    'ZF=F':'Five-Year US Treasury Note Futu',
    'ZT=F':'2-Year T-Note Futures,Jun-2020',
    'GC=F':'Gold',
    'ZG=F':'Gold 100 oz. Apr 20',
    'SI=F':'Silver',
    'ZI=F':'Silver 5000 oz. May 20',
    'PL=F':'Platinum Jul 20',
    'HG=F':'Copper Jul 20',
    'PA=F':'Palladium Sep 20',
    'CL=F':'Crude Oil',
    'HO=F':'Heating Oil Jun 20',
    'NG=F':'Natural Gas Jun 20',
    'RB=F':'RBOB Gasoline Jun 20',
    'BZ=F':'Brent Crude Oil Last Day Financ',
    'B0=F':'Mont Belvieu LDH Propane (OPIS)',
    'C=F':'Corn Jul 20',
    'O=F':'Oats Jul 20',
    'KW=F':'KC HRW Wheat Futures,Jul-2020,C',
    'RR=F':'Rough Rice Jul 20',
    'SM=F':'Soybean Meal Jul 20',
    'BO=F':'Soybean Oil Jul 20',
    'S=F':'Soybeans Jul 20',
    'FC=F':'Feeder Cattle Aug 20',
    'LH=F':'Lean Hogs Jun 20',
    'LC=F':'Live Cattle Jun 20',
    'CC=F':'Cocoa Jul 20',
    'KC=F':'Coffee Jul 20',
    'CT=F':'Cotton Jul 20',
    'LB=F':'Lumber Jul 20',
    'OJ=F':'Orange Juice Jul 20',
    'SB=F':'Sugar #11 Jul 20'
}
dict_treasury_yahoo={
                '^IRX':'13 Week Treasury Bill',
                '^FVX':'Treasury Yield 5 Years',
                '^TNX':'Treasury Yield 10 Years',
                '^TYX':'Treasury Yield 30 Years'
}
dict_currency_yahoo={
                'EURUSD=X':'欧元美元汇率',
                'CNY=X':"人民币美元汇率",
                'JPY=X':'日元美元汇率'
}

normal_list_yahoo=['YM=F','ES=F','NQ=F','RTY=F','CL=F','GC=F','^TNX','^VIX','^FTSE']
worldindics_yahoo=['^GSPC','^DJI','^IXIC','^NYA','^XAX','^BUK100P','^RUT','^VIX','^FTSE','^GDAXI','^FCHI','^STOXX50E','^N100','^BFX','IMOEX.ME','^N225','^HSI','000001.SS','^STI','^AXJO','^AORD','^BSESN','^JKSE','^KLSE','^NZ50','^KS11',
            '^TWII','^GSPTSE','^BVSP','^MXX','^IPSA','^MERV','^TA125.TA','^CASE30','^JN0U.JO']
futures_yahoo=['ES=F','YM=F','NQ=F','RTY=F','ZB=F','ZN=F','ZF=F','ZT=F','GC=F','ZG=F','SI=F','ZI=F','PL=F','HG=F','PA=F','CL=F','HO=F','NG=F','RB=F','B0=F','C=F','O=F','KW=F','RR=F','SM=F','BO=F','S=F','FC=F',
         'LH=F','LC=F','CC=F','KC=F','CT=F','LB=F','OJ=F','SB=F']
treasury_yahoo=['^IRX','^FVX','^TNX','^TYX']
currency_yahoo=['EURUSD=X','CNY=X','JPY=X']
main_kind_yahoo=['BTCUSD=X']
def get_timeseries_result_yahoo(kind,interval=defined_interval):
    defined_wed = 'https://query1.finance.yahoo.com/v8/finance/chart/YM=F?symbol='+kind+'&period1=' + str(
        choiced_timepoint - dict_choiced_timelenth[interval]) + '&period2=' + str(
        choiced_timepoint) + '&interval=' + interval if interval!='1w' else '1d' +'&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=mBUuatSAzmD&corsDomain=finance.yahoo.com'
    header={'Referer':'https://finance.yahoo.com/quote/BTCUSD%3DX/chart?p=BTCUSD%3DX',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Cookie':'A1=d=AQABBAZks14CEDU5h0jSXNPdHRc5cwqclPYFEgEBAQG1tF69XgAAAAAA_SMAAAcIBmSzXgqclPY&S=AQAAAk1JsqQWfnyDkXUd7q8__3Q; A3=d=AQABBAZks14CEDU5h0jSXNPdHRc5cwqclPYFEgEBAQG1tF69XgAAAAAA_SMAAAcIBmSzXgqclPY&S=AQAAAk1JsqQWfnyDkXUd7q8__3Q; B=fd54s19fb6p06&b=3&s=11; GUC=AQEBAQFetLVevUIcaAPl; ucs=lbit=1589266212207; A1S=d=AQABBAZks14CEDU5h0jSXNPdHRc5cwqclPYFEgEBAQG1tF69XgAAAAAA_SMAAAcIBmSzXgqclPY&S=AQAAAk1JsqQWfnyDkXUd7q8__3Q&j=WORLD; PRF=t%3DBTCUSD%253DX'
            }
    param={
        'region':'US',
        'lang':'en-US',
        'includePrePost':'false',
        'events':'div|split|earn',
        'crumb':'mBUuatSAzmD',
        'corsDomain':'finance.yahoo.com'
    }
    gets_result = rs.get(defined_wed,params=param,headers=header)
    kline = [[], []]
    if gets_result.status_code == 200:
        results = js.loads(gets_result.text)
        for k in range(0, len(results['chart']['result'][0]['timestamp'])):
            kline[0].append(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(results['chart']['result'][0]['timestamp'][k])))
            kline[1].append([])
            kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['low'][k])
            kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['high'][k])
            kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['open'][k])
            kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['close'][k])
            kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['volume'][k])
    else:
        print(gets_result.status_code)
    return kline
def realtime_result_aicoin_or_yahoo(kind):
    url = "https://query1.finance.yahoo.com/v7/finance/spark?symbols=" + kind + "&range=1d&interval=5m&indicators=close&includeTimestamps=false&includePrePost=false&corsDomain=finance.yahoo.com&.tsrc=finance"
    get_result = rs.get(url)
    if get_result.status_code == 200:
        results = js.loads(get_result.text)
        print(results['spark']['result'][0]['response'][0]['meta']['regularMarketPrice'])
        return results['spark']['result'][0]['response'][0]['meta']['regularMarketPrice']
    else:
        print("Error", get_result.status_code)
        return None
def realtime_result_innerweb(timelenth=1):
    url = "https://www.aicoin.cn/api/chart/kline/data/period"
    senddatas = {'symbol': "btcusdt:okex", 'period': "1", 'open_time': "24", 'type': "1"}
    header = {'Host': 'www.aicoin.cn', 'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_btcquarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    results = rs.post(url, data=senddatas, headers=header)
    if results.status_code == 200:
        return js.loads(results.text)['data']['kline_data'][len(js.loads(results.text)['data']['kline_data']) - 1][4]
    else:
        url = "https://quote.tubiaojia.com/api/quote/kline?symbol=BTCUSD&type=" + str(timelenth) + "&end=0"
        get_result = rs.get(url)
        if get_result.status_code==200:
            results = js.loads(get_result.text)
            return results['data'][len(results['data']) - 1]['close']
        else:
            print("Error", get_result.status_code)
            return None
def eco_data_yearly():
    countrydict = {'中国': ['1000060'],'美国': ['USA'], '英国': ['GBR'], '法国':['FRA'],'德国':['DEU'],'日本': 'Japan' }
    subject_dict = {
        '人口数量': ['1011030', 'WBWDI2019Jan'],
        '固定价格GDP变动率': ['1003660', 'WBWDI2019Jan'],
        '总储蓄': ['NY.GNS.ICTR.ZS', 'WBWDI2019Jan'],
        '货物和服务进口': ["NE.IMP.GNFS.KD.ZG", 'WBWDI2019Jan'],
        '居民最终消费支出增长率': ['NE.CON.PRVT.KD.ZG', 'WBWDI2019Jan'],
        "失业率": ['SL.UEM.TOTL.ZS', 'WBWDI2019Jan'],
        "经常项目平衡": ['BN.CAB.XOKA.CD', 'WBWDI2019Jan'],
        '存贷利差': ['FR.INR.LEND', 'WBWDI2019Jan'],
        '广义货币增长率': ['FM.LBL.BMNY.ZG', 'WBWDI2019Jan']
    }
    for j in countrydict:
        print(j)
        for k in subject_dict:

            datas = js.dumps({'Header': [
                {"DimensionId": "Time", "Members": [], "DimensionName": "时间", "DatasetId": "WBWDI2019Jan", "Order": 0,
                 "UiMode": "allData"}], "Stub": [
                {"DimensionId": "series", "Members": subject_dict[k][0], "DimensionName": "系列",
                 "DatasetId": "WBWDI2019Jan",
                 "Order": 0}], "Filter": [
                {"DimensionId": "country", "Members": countrydict[j], "DimensionName": "国家", "DatasetId": "WBWDI2019Jan",
                 "Order": 0, "IsGeo": 'true'}], "TimeseriesAttributes": [], "Frequencies": ["A"],
                                "Dataset": "WBWDI2019Jan",
                                "Segments": 'null', "MeasureAggregations": 'null', "Calendar": 0})
            header={
                'Host': 'cn.knoema.com',
                'Content-Type':'Application/json;charset=utf-8',
                'Accept':'*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
                'Origin':'https://cn.knoema.com',
                'Referer':'https://cn.knoema.com/WBWDI2019Jan/%E4%B8%96%E7%95%8C%E5%8F%91%E5%B1%95%E6%8C%87%E6%A0%87',
            }
            print("Begin", k)
            try:
                print(knoema.get(subject_dict[k][1], **{'frequency': 'A', 'Country': countrydict[j][0],'Series': subject_dict[k][0]}).values.tolist())
            except ValueError:
                print("Valueerror")
            except urllib.error.HTTPError:
                print("Internet Error")
            time.sleep(5)
def eco_data_monthly(subject,country):
    countrydict={'美国':'US','中国':'CN','日本':'JP','法国':'FR','德国':'DE','英国':'GB','中国香港':'HK'}
    subject_dict={
        '各国股市指数月度数据':'DSTKMKTXD',
        '外汇储备':'TOTRESV',
        '失业率':'KN.Z8',
        '核心CPI':'KN.CRCPISA',
        '制造业管理人指数PMI':'KN.NS4'
    }
def realtime_depths_btc():
    web_url='https://www.aicoin.cn/api/chart/kline/data/depths'
    search_url="https://www.aicoin.cn/api/chart/market/search"
    header = {'Host': 'www.aicoin.cn', 'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_btcquarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    search_result=js.loads(rs.post(search_url,data={'key':'btc USD','page_size':'50','lan':'cn','open_time':'24'},headers=header).text)
    website_list=[]
    if search_result!=None:
        for i in search_result['data']['list']:
            website_list.append([i['market_name'],i['key']])

    for k in range(0,len(website_list)):
        time.sleep(random.uniform(0,5))
        results=rs.post(web_url,data={'symbol':website_list[k][1]},headers=header)
        if results.status_code==200:
            results_json=js.loads(results.text)['data']
            website_list[k].append(results_json)
            print((k+1)*100/len(website_list),"%",website_list[k][0],'finished')
        else:
            print("Error",results.status_code)
            return website_list
    return website_list


