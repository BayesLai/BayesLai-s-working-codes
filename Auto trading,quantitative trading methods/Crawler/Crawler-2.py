
from requests import get,post
from json import loads,dumps
from random import normalvariate,uniform
from statsmodels.api import OLS
from statsmodels.api import add_constant
from sklearn.decomposition import PCA
import pandas
import time
import pandas as pd
from sys import exc_info
from csv import writer
from matplotlib.pyplot import plot ,show
class kline(object):
    def __init__(self):
        self.openpriceline=[]
        self.closepriceline=[]
        self.highpriceline=[]
        self.lowpriceline=[]
        self.timestamp=[]
        self.str_timestamp=self.timestamptostr()
        self.volume=[]
    def timestamptostr(self):
        self.str_timestamp=[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in self.timestamp]
    def self_lengthadjust(self):
        if self.timestamp!=None and self.str_timestamp==None:
            self.timestamptostr()
            dp.timeserieslength_adjust([self.openpriceline,self.closepriceline,self.highpriceline,self.lowpriceline,self.timestamp,self.str_timestamp])
        elif self.timestamp!=None and self.str_timestamp!=None:
            dp.timeserieslength_adjust(
                [self.openpriceline, self.closepriceline, self.highpriceline, self.lowpriceline, self.timestamp,
                 self.str_timestamp])
        else:
            self.timestamp=None
            self.str_timestamp=None
            dp.timeserieslength_adjust(
                [self.openpriceline, self.closepriceline, self.highpriceline, self.lowpriceline])

defined_interval='1d'
choiced_timepoint=int(time.time())
dict_choiced_timelenth={
    '1m':60*60*24,
    '2m':60*60*24*2,
    '5m':60*60*24*5,
    '15m':60*60*24*15,
    '30m':60*60*24*30,
    '60m':60*60*24*60,
    '1d':60*60*24*365*3,
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
dict_quick_list_yahoo={
                        'YM=F':[{'道琼斯指数期货':'DOW Futures'}],
                 'CL=F':[{'原油价格指数':'NY Mercantile - NY Mercantile Delayed Price. Currency in USD'}],
                 'GC=F':[{'黄金COMEX期货价格指数':'Gold - COMEX Delayed Price. Currency in USD'}],
                 '^VIX':[{'波动率指数(恐慌指数)':'CBOE Volatility Index-Chicago Options - Chicago Options Delayed Price. Currency in USD'}],
'^FTSE':[{'富时100指数':'FTSE Index - FTSE Index Delayed Price. Currency in GBP'}],
                 '000001.SS':[{'中国上证A股综合指数':'SSE Composite Index'}],
'^N225':[{'日经指数':'Nikkei 225'}],
                '^IRX': '13 Week Treasury Bill',
'PL=F':'Platinum Jul 20',
                'HG=F':'Copper Jul 20',
                'FC=F':'Feeder Cattle Aug 20',
                'EURUSD=X':'欧元美元汇率',
                'C=F':'小麦Corn Jul 20',
    'PA=F':'钯- Palladium Sep 20',
    'NG=F':'Natural Gas Jun 20',
    'RR=F':'Rough Rice Jul 20',
    'SM=F':'豆粕Soybean Meal Jul 20',
    'LH=F':'Lean Hogs Jun 20',
    'CC=F':'Cocoa Jul 20',
    'KC=F':'Coffee Jul 20',
    'CT=F':'Cotton Jul 20',
    'LB=F':'Lumber Jul 20',
    'SB=F':'Sugar #11 Jul 20'
} 

dict_normal_list_yahoo={
                        'YM=F':[{'道琼斯指数期货':'DOW Futures'}],
                     'ES=F':[{'标准普尔500期货':'S&P Futures'}],
                     'NQ=F':[{'纳斯达克指数期货':'Nasdaq Futures'}],
                     'RTY=F':[{'罗素2000指数期货':'Russell 2000 Futures'}],
                 'CL=F':[{'原油价格指数':'NY Mercantile - NY Mercantile Delayed Price. Currency in USD'}],
                 'GC=F':[{'黄金COMEX期货价格指数':'Gold - COMEX Delayed Price. Currency in USD'}],
                 '^TNX':[{'美国十年国债收益率':'Treasury Yield 10 Years'}],
                 '^VIX':[{'波动率指数(恐慌指数)':'CBOE Volatility Index-Chicago Options - Chicago Options Delayed Price. Currency in USD'}],
                 '^FTSE':[{'富时100指数':'FTSE Index - FTSE Index Delayed Price. Currency in GBP'}],
                 '000001.SS':[{'中国上证A股综合指数':'SSE Composite Index'}],
                 '^N225':[{'日经指数':'Nikkei 225'}],
                'ZF=F':[{'五年美国国库券价格':'Five-Year US Treasury Note Futu'}],
                    'ZT=F':[{'两年美国国库券价格':'2-Year T-Note Futures,Jun-2020'}],
                '^IRX': '13 Week Treasury Bill',
                '^FVX': 'Treasury Yield 5 Years',
                '^TYX': 'Treasury Yield 30 Years',
                'PL=F':'Platinum Jul 20',
                'HG=F':'Copper Jul 20',
                'FC=F':'Feeder Cattle Aug 20',
                'EURUSD=X':'欧元美元汇率',
                'C=F':'小麦Corn Jul 20',
    'PA=F':'钯- Palladium Sep 20',
    'NG=F':'Natural Gas Jun 20',
    'RB=F':'RBOB Gasoline Jun 20',
    'B0=F':'Mont Belvieu LDH Propane (OPIS)',
    'O=F':'Oats Jul 20',
    'KW=F': 'KC HRW Wheat Futures,Jul-2020,C',
    'RR=F': 'Rough Rice Jul 20',
    'SM=F': '豆粕Soybean Meal Jul 20',
    'BO=F': 'Soybean Oil Jul 20',
    'S=F': 'Soybeans Jul 20',
    'LH=F': 'Lean Hogs Jun 20',
    'LC=F': 'Live Cattle Jun 20',
    'CC=F': 'Cocoa Jul 20',
'SB=F':'Sugar #11 Jul 20'  ,
    'KC=F': 'Coffee Jul 20',
    'CT=F': 'Cotton Jul 20',
    'LB=F': 'Lumber Jul 20',
    'CNY=X': "人民币美元汇率",
     'JPY=X': '日元美元汇率',
    'OJ=F':'Orange Juice Jul 20'
}
dict_all_list_yahoo={
'^GSPC':'S&P 500',
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
                  '^JN0U.JO':'Top 40 USD Net TRI Index',
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
    'SB=F':'Sugar #11 Jul 20',
    '^IRX': '13 Week Treasury Bill',
    '^FVX': 'Treasury Yield 5 Years',
    '^TNX': 'Treasury Yield 10 Years',
    '^TYX': 'Treasury Yield 30 Years',
'EURUSD=X':'欧元美元汇率',
                'CNY=X':"人民币美元汇率",
                'JPY=X':'日元美元汇率'
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
    defined_wed = 'https://query1.finance.yahoo.com/v8/finance/chart/'+kind+'?symbol'+kind+'&period1=' + str(
        choiced_timepoint - dict_choiced_timelenth[interval]) + '&period2=' + str(
        choiced_timepoint) + '&interval=' + interval  +'&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=mBUuatSAzmD&corsDomain=finance.yahoo.com'
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
    gets_result = get(defined_wed,params=param,headers=header)
    kline = [[], [],[]]
    if gets_result.status_code == 200:
        results = loads(gets_result.text)
        try :
            for k in range(0, len(results['chart']['result'][0]['timestamp'])):
                kline[2].append(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(results['chart']['result'][0]['timestamp'][k])))
                kline[1].append([])
                kline[0].append(results['chart']['result'][0]['timestamp'][k])
                kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['low'][k])
                kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['high'][k])
                kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['open'][k])
                kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['close'][k])
                kline[1][len(kline[1]) - 1].append(results['chart']['result'][0]['indicators']['quote'][0]['volume'][k])
        except KeyError:
            print("------------------Error------------------")
            print(results)
            return []
    else:
        print(gets_result.status_code)
    return kline
def realtime_newestprice_aicoin(symbol):#爬取收盘价
    url ='https://www.aicoin.cn/api/chart/kline/data/trades'
    send_data={
        'symbol':symbol+'swapusd:okcoinfutures'
    }
    header = {'Referer': 'https://www.aicoin.cn/chart/hbdm_btccqusd',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Host':'www.aicoin.cn'
              }
    get_result = post(url,data=send_data,headers=header)
    if get_result.status_code == 200:
        results = loads(get_result.text)
        closepriceline=[]
        for i in results['data']:
            closepriceline.append(float(i['price']))
        return closepriceline
    else:
        print("Error", get_result.status_code)
        return None
def realtime_klineprice_aicoin(symbol,interval):#爬取k线数据
    symbol=symbol.lower()
    kx=interval.find('m' or 'd')
    interval=interval[:kx]if interval!='1d' else '1440'
    url = 'https://www.aicoin.cn/api/chart/kline/data/period'
    send_data = {
        'symbol': symbol + 'swapusd:okcoinfutures',
        'period':interval,
        'open_time':'24',
        'type':'1'
    }
    header = {'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_'+symbol+'quarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Host': 'www.aicoin.cn'
              }
    my_kline=kline()
    get_result = post(url, data=send_data, headers=header)
    if get_result.status_code == 200:
        results = loads(get_result.text)
        try:
            for i in results['data']['kline_data']:
                my_kline.openpriceline.append(float(i[1]))
                my_kline.closepriceline.append(float(i[2]))
                my_kline.lowpriceline.append(float(i[3]))
                my_kline.highpriceline.append(float(i[4]))
                my_kline.timestamp.append(float(i[0]))
        except KeyError:
            print(results)
        if my_kline.closepriceline==[]:
            print(symbol.upper(),'error')
        return my_kline
    else:
        print("Error", get_result.status_code)
        return None
def realtime_result_innerweb(timelenth=1):
    url = "https://www.aicoin.cn/api/chart/kline/data/period"
    senddatas = {'symbol': "btcusdt:okex", 'period': "1", 'open_time': "24", 'type': "1"}
    header = {'Host': 'www.aicoin.cn', 'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_btcquarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    results = post(url, data=senddatas, headers=header)
    if results.status_code == 200:
        return loads(results.text)['data']['kline_data'][len(loads(results.text)['data']['kline_data']) - 1][4]
    else:
        url = "https://quote.tubiaojia.com/api/quote/kline?symbol=BTCUSD&type=" + str(timelenth) + "&end=0"
        get_result = get(url)
        if get_result.status_code==200:
            results = loads(get_result.text)
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
        "失业率": ['SL.UEM.TOTL.ZS', 'WBWDI2019Jan'],
        '存贷利差': ['FR.INR.LEND', 'WBWDI2019Jan'],
        '广义货币增长率': ['FM.LBL.BMNY.ZG', 'WBWDI2019Jan']
    }
    for j in countrydict:
        print(j)
        for k in subject_dict:
            datas = dumps({'Header': [
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

def realtime_depths(symbol):
    web_url='https://www.aicoin.cn/api/chart/kline/data/depths'
    header = {'Host': 'www.aicoin.cn', 'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_btcquarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

    send_data={
        'symbol':symbol
    }
    depths={
        'asks':[[],[]],
        'bids':[[],[]]
    }
    depth_result=post(web_url,data=send_data,headers=header)
    if depth_result.status_code==200:
        json_result=loads(depth_result.text)
        if json_result['data']!=[] and json_result['data']['asks']!=[] and json_result['data']['bids']!=[]:
            for index_asks in range(0,len(json_result['data']['asks'])):
                depths['asks'][0].append(float(json_result['data']['asks'][index_asks][0]))
                depths['asks'][1].append(float(json_result['data']['asks'][index_asks][1]))
            for index_bids in range(0,len(json_result['data']['bids'])):
                depths['bids'][0].append(float(json_result['data']['bids'][index_bids][0]))
                depths['bids'][1].append(float(json_result['data']['bids'][index_bids][1]))
            return depths
        else:
            raise ValueError("全是空列表")
    else:
        raise ValueError("网络错误",depth_result.status_code,"|",exc_info())
def get_all_crptocurrency_list():
    url="https://www.aicoin.cn/api/chart/market/search"
    curr_page_list=[]
    total_result=[]
    standard_save_object={
        'symbol':None,
        'market_name':None,
        'name':None,
        'currency_str':None,
        'long_name':None
    }
    header = {'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_btcquarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Host': 'www.aicoin.cn',
              'Origin':'https://www.aicoin.cn'
              }
    curr_page_list.append("")
    for i in range (2,78):
        curr_page_list.append(str(i))
    for curr_age in curr_page_list:
        senddata={
            'only_match':"0",
            'key':'',
            'page_size':'50',
            'curr_page':curr_age,
            'lan':'cn',
            'open_time':'24'
        } if curr_page_list.index(curr_age)!=0 else {
            'only_match':"0",
            'key':'',
            'page_size':'50',
            'lan':'cn',
            'open_time':'24'
        }
        time.sleep(abs(normalvariate(0,1.25)))
        post_result=post(url,data=senddata,headers=header)
        if post_result.status_code==200:
            text_json=loads(post_result.text)
            for each_data in text_json['data']['list']:
                new_save_object = standard_save_object.copy()
                new_save_object['symbol']=each_data['key']
                new_save_object['name']=each_data['coin_show']
                new_save_object['market_name']=each_data['market_name']
                new_save_object['currency_str']=each_data['currency_str']
                new_save_object['long_name']=each_data['symbol']
                total_result.append(new_save_object)
                print("添加",new_save_object,"完毕")
        else:
            raise AttributeError("没能连接得到数据:",post_result.status_code)

    return total_result


def realtime_klineprice_aicoin_bysymbol(symbol,interval):#爬取k线数据
    interval=str(interval)
    url = 'https://www.aicoin.cn/api/chart/kline/data/period'
    send_data = {
        'symbol': symbol ,
        'period':interval,
        'open_time':'24',
        'type':'1'
    }
    header = {'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_'+symbol+'quarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Host': 'www.aicoin.cn'
              }
    my_kline=kline()
    get_result = post(url, data=send_data, headers=header)
    if get_result.status_code == 200:
        results = loads(get_result.text)
        try:
            for i in results['data']['kline_data']:
                my_kline.openpriceline.append(float(i[1]))
                my_kline.closepriceline.append(float(i[2]))
                my_kline.lowpriceline.append(float(i[3]))
                my_kline.highpriceline.append(float(i[4]))
                my_kline.volume.append(float(i[5]))
                my_kline.timestamp.append(float(i[0]))
        except KeyError:
            print(results)
        if my_kline.closepriceline==[]:
            print(symbol.upper(),'error')
        return my_kline
    else:
        print("Error", get_result.status_code)
        return None
#get_all_crptocurrency_list()
def realtime_order_okex_bysymbol(symbol):
    url="https://www.okex.me/v2/perpetual/pc/public/contracts/"+symbol+"/depth?t="+str(int(time.time()))
    order_line={
        'buy':{
            'priceline':[],
            'requests':[]
        }
            ,
            'sell':{
                'priceline': [],
                'requests': []
            }
    }
    todata={
        't':str(int(time.time()))
    }
    header_s={
        'Referer':'https://www.okex.me/derivatives/swap/full/usd-btc',
        'Host':'www.okex.me',
        'User-Agent':'https://www.okex.me/v2/perpetual/pc/public/contracts/BTC-USD-SWAP/depth?t=1595313799068'
    }
    get_results=get(url,data=todata,headers=header_s)
    if get_results.status_code==200:
        try:
            json_result=loads(get_results.text)
        except:
            raise ValueError("错误:", exc_info())
        for i in range(0,len(json_result['data']['asks'])):
            order_line['sell']['priceline'].append(float(json_result['data']['asks'][i][0]))
            order_line['sell']['requests'].append(float(json_result['data']['asks'][i][1]))
        for i in range(0,len(json_result['data']['bids'])):
            order_line['buy']['priceline'].append(float(json_result['data']['bids'][i][0]))
            order_line['buy']['requests'].append(float(json_result['data']['bids'][i][1]))
    else:
        print(get_results.status_code)
        raise ValueError("错误:",exc_info())
    return order_line

def realtime_fundflow_okex_bysymbol(symbol):
    url="https://www.okex.me/v2/perpetual/pc/public/contracts/"+symbol+"/lastDeal?t="+str(int(time.time()))
    list_fundflow=[[],[],[]]
    get_results=get(url)
    if get_results.status_code==200:
        json_result=loads(get_results.text)
        for i in range(0,len(json_result['data'])):
            list_fundflow[0].append(float(json_result['data'][i]['price']))
            list_fundflow[1].append(1 if json_result['data'][i]['side']=='buy' else -1)
            list_fundflow[2].append(float(json_result['data'][i]['size']))
        return list_fundflow
    else:
        print(get_results.status_code)
        raise ValueError("错误:",exc_info())

def get_aioin_detail_bysymbol(symbol):
    url='https://www.aicoin.cn/api/chart/market/coin/detail'
    header = {'Referer': 'https://www.aicoin.cn/chart/okcoinfutures_' + symbol + 'quarter',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
              'Host': 'www.aicoin.cn'
              }
    send_data = {
        'symbol': symbol
    }
    get_result = post(url, data=send_data, headers=header)
    json_result = loads(get_result.text)
    if get_result.status_code == 200 and json_result['data']!=None:
        return json_result['data']['detail']
    elif get_result.status_code != 200:
        raise ValueError("网络错误", get_result.status_code)
    else:
        raise ValueError("数据为空")
