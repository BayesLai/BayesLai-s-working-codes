import AIchoice as ac
import Crawler as cr
import DataProcess as dp
import matplotlib.pyplot as mat
import threading
from queue import  Queue
from time import time,sleep
import MarcoIndex as MI
import tkinter

import csv
fee=0.0003 #算两次，下单成交和清仓成交各收当时价格的这个比例

'''
预定义数据集
'''
list_yahoo_crypto=[
'BTC-USD',
'ETH-USD',
'XRP-USD',
'USDT-USD',
'BCH-USD',
'LTC-USD',
#'BNB-USD',
'EOS-USD',
'XLM-USD',
'ADA-USD',
'LINK-USD',
'XMR-USD',
'TRX-USD',
'ETC-USD',
'NEO-USD',
'DASH-USD',
'MIOTA-USD',
'ZEC-USD',
'XEM-USD',
'DOGE-USD',
'BAT-USD',
'DGB-USD',
'VET-USD',
'ZRX-USD',
'DCR-USD',
'BTG-USD',
'DCR-USD',
'ICX-USD',
'QTUM-USD',
'REP-USD',
'LSK-USD',
'OMG-USD',
'KNC-USD',
'WAVES-USD',
'NANO-USD',
'SNT-USD',
'MONA-USD',
'MCO-USD',
'SC-USD',
'STEEM-USD',
'KMD-USD',
'XVG-USD',
'BTS-USD',
'ZEN-USD',
'HC-USD',
'GNT-USD',
'BCN-USD',
'XZC-USD',
'MAID-USD',
'LRC-USD',
'ARDR-USD',
'ANT-USD',
'AE-USD',
]
aicoin_crypto_list=[]
for i in list_yahoo_crypto:
    tx=i.find('-')
    aicoin_crypto_list.append(i[:tx])
dict_timelength={
    '5m':60*3.5,
    '15m':60*14,
    '30m':60*29,
    '60m':60*59,
    '1d':60*60*24-60*3
}


class btc_test(object):
    def __init__(self,interval):
        if interval in dict_timelength:
            self.last_update_time = time()
            self.interval = interval

            self.klines=MI.klines_symbolprice_at_interval(symbol='BTC', interval=self.interval)
            self.last_update_time = time()
            self.top_list=[]
            self.status=0 #0,1表示做了一个多单,-1表示做了一空单
            self.yield_rate=1 #按收益率计算更好
            self.last_price=0 #这里是当前订单的成本价，当没有交易的时候，这个是None
            self.now_price=0 #现价，初始化为None
            self.realtime_yield=1
            with open("btc-test-record-"+interval+".csv", 'r')as mywriter:
                readers = list(csv.reader(mywriter))
                if len(readers) != 0 and readers[len(readers) - 1]!=None:
                    try:
                        self.status = int(readers[len(readers) - 1][1])
                        self.last_price = float(readers[len(readers) - 1][2])
                        self.yield_rate = float(readers[len(readers) - 1][3])
                    except:
                        pass

                    if self.status==1:
                        print('更新完毕:上次未完成订单的状态%s,上次未完成订单的价格%f,累计收益率%f' % ("做多" , self.last_price  , self.yield_rate))
                    elif self.status==-1:
                        print('更新完毕:上次未完成订单的状态%s,上次未完成订单的价格%f,累计收益率%f' % (
                        "做空", self.last_price  , self.yield_rate))
                    else:
                        print('更新完毕:上次未完成订单的状态%s,上次未完成订单的价格%f,累计收益率%f' % (
                        " 无 ", self.last_price, self.yield_rate))
            self.multiasset_object = MI.klines_multiasset_at_interval(self.interval)

        else:
            raise KeyError('类型错误,当前选择的时间周期不可支持')
    def update_myself(self):
        self.multiasset_object.update()
        self.klines.update(self.multiasset_object)
        self.last_update_time = time()

my_test=btc_test('5m')
now_priceline = cr.realtime_klineprice_aicoin('BTC','5m').closepriceline
now_price=now_priceline[len(now_priceline)-1]

my_test2=btc_test('15m')
now_priceline2 = cr.realtime_klineprice_aicoin('BTC','15m').closepriceline
now_price2=now_priceline[len(now_priceline)-1]

my_test3=btc_test('30m')
now_priceline3 = cr.realtime_klineprice_aicoin('BTC','30m').closepriceline
now_price3=now_priceline[len(now_priceline)-1]

my_test4=btc_test('60m')
now_priceline4 = cr.realtime_klineprice_aicoin('BTC','60m').closepriceline
now_price4=now_priceline[len(now_priceline)-1]
while True:
    if time()-my_test.last_update_time-dict_timelength['5m']>0:
        now_priceline = cr.realtime_klineprice_aicoin('BTC','5m').closepriceline
        now_price=now_priceline[len(now_priceline)-1]
        my_test.update_myself()
        if my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline)-1]<=-1 and my_test.status==0:
            my_test.status=1
            my_test.last_price=now_priceline[len(now_priceline)-1]
            my_test.yield_rate=my_test.yield_rate*(1-fee)
            with open('btc-test-record.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test.status, my_test.last_price ,
                                 my_test.yield_rate, now_price, my_test.klines.index_kline.closepriceline[
                                     len(my_test.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test.realtime_yield=my_test.yield_rate*(1+my_test.status*(now_price-my_test.last_price)/my_test.last_price)
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test.status if my_test.status != None else 0, my_test.yield_rate,
                my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],my_test.realtime_yield,
                now_price))
        elif my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline)-1]>=1 and my_test.status==0:
            my_test.status = -1
            my_test.last_price = now_priceline[len(now_priceline)-1]
            my_test.yield_rate = my_test.yield_rate * (1 - fee)
            with open('btc-test-record.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test.status, my_test.last_price ,
                                 my_test.yield_rate, now_price, my_test.klines.index_kline.closepriceline[
                                     len(my_test.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                        now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test.status if my_test.status != None else 0, my_test.yield_rate,
                my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                my_test.realtime_yield,
                now_price))
        elif my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline)-1]<=-1 and my_test.status!=0:
            if my_test.status==-1:
                my_test.yield_rate=my_test.yield_rate*(1-fee)*(1-(now_price-my_test.last_price)/my_test.last_price) if my_test.last_price!=0 else my_test.yield_rate
                my_test.status = 1
                my_test.last_price = now_priceline[len(now_priceline)-1]
                my_test.yield_rate = my_test.yield_rate * (1 - fee)
                with open('btc-test-record.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test.status, my_test.last_price ,
                                     my_test.yield_rate, now_price, my_test.klines.index_kline.closepriceline[
                                         len(my_test.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                            now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test.status if my_test.status != None else 0, my_test.yield_rate,
                    my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                    my_test.realtime_yield,
                    now_price))
            else:
                my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                            now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test.status if my_test.status != None else 0, my_test.yield_rate,
                    my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                    my_test.realtime_yield,
                    now_price))
        elif my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline)-1]>=1 and my_test.status!=0:
            if my_test.status==1:
                my_test.yield_rate=my_test.yield_rate*(1-fee)*(1+(now_price-my_test.last_price)/my_test.last_price)
                my_test.status = -1
                my_test.last_price =now_priceline[len(now_priceline)-1]
                my_test.yield_rate = my_test.yield_rate * (1 - fee)
                with open('btc-test-record.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test.status, my_test.last_price ,
                                     my_test.yield_rate, now_price, my_test.klines.index_kline.closepriceline[
                                         len(my_test.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                            now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test.status if my_test.status != None else 0, my_test.yield_rate,
                    my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                    my_test.realtime_yield,
                    now_price))
            else:
                my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                            now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test.status , my_test.yield_rate,
                    my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                    my_test.realtime_yield,
                    now_price))
        elif -1<=my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline)-1]<=1 and my_test.status!=0:

            my_test.yield_rate=my_test.yield_rate*(1-fee)*(1+my_test.status*(now_price-my_test.last_price)/my_test.last_price) if my_test.last_price!=0 else my_test.yield_rate


            my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                        now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test.status if my_test.status != 0 else 0, my_test.yield_rate,
                my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                my_test.realtime_yield,
                now_price))
            my_test.status = 0
            my_test.last_price = 0
            with open('btc-test-record.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test.status, my_test.last_price ,
                                 my_test.yield_rate, now_price, my_test.klines.index_kline.closepriceline[
                                     len(my_test.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
        else:
            my_test.realtime_yield = my_test.yield_rate * (1 + my_test.status * (
                        now_price - my_test.last_price) / my_test.last_price) if my_test.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test.status if my_test.status !=0 else 0, my_test.yield_rate,
                my_test.klines.index_kline.closepriceline[len(my_test.klines.index_kline.closepriceline) - 1],
                my_test.realtime_yield,
                now_price))
    else:
        print("---------------------------------------------")
        sleep(20)
        
    if time()-my_test2.last_update_time-dict_timelength['15m']>0:
        now_priceline2 = cr.realtime_klineprice_aicoin('BTC','15m').closepriceline
        now_price2=now_priceline2[len(now_priceline2)-1]
        my_test2.update_myself()
        if my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline)-1]<=-1 and my_test2.status==0:
            my_test2.status=1
            my_test2.last_price=now_priceline2[len(now_priceline2)-1]
            my_test2.yield_rate=my_test2.yield_rate*(1-fee)
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test2.status, my_test2.last_price ,
                                 my_test2.yield_rate, now_price, my_test2.klines.index_kline.closepriceline[
                                     len(my_test2.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test2.realtime_yield=my_test2.yield_rate*(1+my_test2.status*(now_price2-my_test2.last_price)/my_test2.last_price) if my_test2.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test2.status if my_test2.status != None else 0, my_test2.yield_rate,
                my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],my_test2.realtime_yield,
                now_price2))
        elif my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline)-1]>=1 and my_test2.status==0:
            my_test2.status = -1
            my_test2.last_price = now_priceline2[len(now_priceline2)-1]
            my_test2.yield_rate = my_test2.yield_rate * (1 - fee)
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test2.status, my_test2.last_price ,
                                 my_test2.yield_rate, now_price, my_test2.klines.index_kline.closepriceline[
                                     len(my_test2.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                        now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test2.status if my_test2.status != None else 0, my_test2.yield_rate,
                my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                my_test2.realtime_yield,
                now_price))
        elif my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline)-1]<=-1 and my_test2.status!=0:
            if my_test2.status==-1:
                my_test2.yield_rate=my_test2.yield_rate*(1-fee)*(1-(now_price2-my_test2.last_price)/my_test2.last_price) if my_test2.last_price!=0 else my_test2.yield_rate
                my_test2.status = 1
                my_test2.last_price = now_priceline2[len(now_priceline2)-1]
                my_test2.yield_rate = my_test2.yield_rate * (1 - fee)
                with open('btc-test-record-30m.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test2.status, my_test2.last_price ,
                                     my_test2.yield_rate, now_price2, my_test2.klines.index_kline.closepriceline[
                                         len(my_test2.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                            now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test2.status if my_test2.status != None else 0, my_test2.yield_rate,
                    my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                    my_test2.realtime_yield,
                    now_price2))
            else:
                my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                            now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test2.status if my_test2.status != None else 0, my_test2.yield_rate,
                    my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                    my_test2.realtime_yield,
                    now_price2))
        elif my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline)-1]>=1 and my_test2.status!=0:
            if my_test2.status==1:
                my_test2.yield_rate=my_test2.yield_rate*(1-fee)*(1+(now_price2-my_test2.last_price)/my_test2.last_price)
                my_test2.status = -1
                my_test2.last_price = now_priceline2[len(now_priceline2)-1]
                my_test2.yield_rate = my_test2.yield_rate * (1 - fee)
                with open('btc-test-record-30m.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test2.status, my_test2.last_price ,
                                     my_test2.yield_rate, now_price2, my_test2.klines.index_kline.closepriceline[
                                         len(my_test2.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                            now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test2.status if my_test2.status != None else 0, my_test2.yield_rate,
                    my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                    my_test2.realtime_yield,
                    now_price2))
            else:
                my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                            now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test2.status , my_test2.yield_rate,
                    my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                    my_test2.realtime_yield,
                    now_price2))
        elif -1<=my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline)-1]<=1 and my_test2.status!=0:

            my_test2.yield_rate=my_test2.yield_rate*(1-fee)*(1+my_test2.status*(now_price2-my_test2.last_price)/my_test2.last_price) if my_test2.last_price!=0 else my_test2.yield_rate


            my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                        now_price2 - my_test2.last_price) / my_test2.last_price) if my_test2.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test2.status if my_test2.status != 0 else 0, my_test2.yield_rate,
                my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                my_test2.realtime_yield,
                now_price2))
            my_test2.status = 0
            my_test2.last_price = 0
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test2.status, my_test2.last_price ,
                                 my_test2.yield_rate, now_price2, my_test2.klines.index_kline.closepriceline[
                                     len(my_test2.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
        else:
            my_test2.realtime_yield = my_test2.yield_rate * (1 + my_test2.status * (
                        now_price2 - my_test2.last_price) / my_test2.last_price)  if my_test2.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test2.status if my_test2.status !=0 else 0, my_test2.yield_rate,
                my_test2.klines.index_kline.closepriceline[len(my_test2.klines.index_kline.closepriceline) - 1],
                my_test2.realtime_yield,
                now_price2))
      
    if time()-my_test3.last_update_time-dict_timelength['30m']>0:
        now_priceline3 = cr.realtime_klineprice_aicoin('BTC','30m').closepriceline
        now_price3=now_priceline3[len(now_priceline3)-1]
        my_test3.update_myself()
        if my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline)-1]<=-1 and my_test3.status==0:
            my_test3.status=1
            my_test3.last_price=now_priceline3[len(now_priceline3)-1]
            my_test3.yield_rate=my_test3.yield_rate*(1-fee)
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test3.status, my_test3.last_price ,
                                 my_test3.yield_rate, now_price, my_test3.klines.index_kline.closepriceline[
                                     len(my_test3.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test3.realtime_yield=my_test3.yield_rate*(1+my_test3.status*(now_price3-my_test3.last_price)/my_test3.last_price) if my_test3.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
            my_test3.status if my_test3.status != None else 0, my_test3.yield_rate,
                my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],my_test3.realtime_yield,
                now_price3))
        elif my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline)-1]>=1 and my_test3.status==0:
            my_test3.status = -1
            my_test3.last_price = now_priceline3[len(now_priceline3)-1]
            my_test3.yield_rate = my_test3.yield_rate * (1 - fee)
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test3.status, my_test3.last_price ,
                                 my_test3.yield_rate, now_price, my_test3.klines.index_kline.closepriceline[
                                     len(my_test3.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                        now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test3.status if my_test3.status != None else 0, my_test3.yield_rate,
                my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                my_test3.realtime_yield,
                now_price))
        elif my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline)-1]<=-1 and my_test3.status!=0:
            if my_test3.status==-1:
                my_test3.yield_rate=my_test3.yield_rate*(1-fee)*(1-(now_price3-my_test3.last_price)/my_test3.last_price) if my_test3.last_price!=0 else my_test3.yield_rate
                my_test3.status = 1
                my_test3.last_price = now_priceline3[len(now_priceline3)-1]
                my_test3.yield_rate = my_test3.yield_rate * (1 - fee)
                with open('btc-test-record-30m.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test3.status, my_test3.last_price ,
                                     my_test3.yield_rate, now_price3, my_test3.klines.index_kline.closepriceline[
                                         len(my_test3.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                            now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test3.status if my_test3.status != None else 0, my_test3.yield_rate,
                    my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                    my_test3.realtime_yield,
                    now_price3))
            else:
                my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                            now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test3.status if my_test3.status != None else 0, my_test3.yield_rate,
                    my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                    my_test3.realtime_yield,
                    now_price3))
        elif my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline)-1]>=1 and my_test3.status!=0:
            if my_test3.status==1:
                my_test3.yield_rate=my_test3.yield_rate*(1-fee)*(1+(now_price3-my_test3.last_price)/my_test3.last_price)
                my_test3.status = -1
                my_test3.last_price = now_priceline3[len(now_priceline3)-1]
                my_test3.yield_rate = my_test3.yield_rate * (1 - fee)
                with open('btc-test-record-30m.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test3.status, my_test3.last_price ,
                                     my_test3.yield_rate, now_price3, my_test3.klines.index_kline.closepriceline[
                                         len(my_test3.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
                my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                            now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test3.status if my_test3.status != None else 0, my_test3.yield_rate,
                    my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                    my_test3.realtime_yield,
                    now_price3))
            else:
                my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                            now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                    my_test3.status , my_test3.yield_rate,
                    my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                    my_test3.realtime_yield,
                    now_price3))
        elif -1<=my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline)-1]<=1 and my_test3.status!=0:

            my_test3.yield_rate=my_test3.yield_rate*(1-fee)*(1+my_test3.status*(now_price3-my_test3.last_price)/my_test3.last_price) if my_test3.last_price!=0 else my_test3.yield_rate


            my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                        now_price3 - my_test3.last_price) / my_test3.last_price) if my_test3.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test3.status if my_test3.status != 0 else 0, my_test3.yield_rate,
                my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                my_test3.realtime_yield,
                now_price3))
            my_test3.status = 0
            my_test3.last_price = 0
            with open('btc-test-record-30m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test3.status, my_test3.last_price ,
                                 my_test3.yield_rate, now_price3, my_test3.klines.index_kline.closepriceline[
                                     len(my_test3.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
        else:
            my_test3.realtime_yield = my_test3.yield_rate * (1 + my_test3.status * (
                        now_price3 - my_test3.last_price) / my_test3.last_price)  if my_test3.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test3.status if my_test3.status !=0 else 0, my_test3.yield_rate,
                my_test3.klines.index_kline.closepriceline[len(my_test3.klines.index_kline.closepriceline) - 1],
                my_test3.realtime_yield,
                now_price3))


    if time()-my_test4.last_update_time-dict_timelength['60m']>0:
        now_priceline4 = cr.realtime_klineprice_aicoin('BTC','60m').closepriceline
        now_price4=now_priceline4[len(now_priceline4)-1]
        my_test4.update_myself()
        if my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline)-1]<=-1 and my_test4.status==0:
            my_test4.status=1
            my_test4.last_price=now_priceline4[len(now_priceline4)-1]
            my_test4.yield_rate=my_test4.yield_rate*(1-fee)
            with open('btc-test-record-60m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test4.status, my_test4.last_price ,
                                 my_test4.yield_rate, now_price, my_test4.klines.index_kline.closepriceline[
                                     len(my_test4.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
            my_test4.realtime_yield=my_test4.yield_rate*(1+my_test4.status*(now_price4-my_test4.last_price)/my_test4.last_price) if my_test4.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test4.status if my_test4.status != None else 0, my_test4.yield_rate,
                my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],my_test4.realtime_yield,
                now_price4))
        elif my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline)-1]>=1 and my_test4.status==0:
            my_test4.status = -1
            my_test4.last_price = now_priceline4[len(now_priceline4)-1]
            my_test4.yield_rate = my_test4.yield_rate * (1 - fee)
            with open('btc-test-record-60m.csv', 'a', newline='') as files:
                    mywriter = csv.writer(files)
                    data_to_write = [time(), my_test4.status, my_test4.last_price ,
                                 my_test4.yield_rate, now_price, my_test4.klines.index_kline.closepriceline[
                                     len(my_test4.klines.index_kline.closepriceline) - 1]]
                    mywriter.writerow(data_to_write)
            my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                        now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
            my_test4.status if my_test4.status != None else 0, my_test4.yield_rate,
            my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                my_test4.realtime_yield,
                now_price))
        elif my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline)-1]<=-1 and my_test4.status!=0:
            if my_test4.status==-1:
                my_test4.yield_rate=my_test4.yield_rate*(1-fee)*(1-(now_price4-my_test4.last_price)/my_test4.last_price) if my_test4.last_price!=0 else my_test4.yield_rate
                my_test4.status = 1
                my_test4.last_price = now_priceline4[len(now_priceline4)-1]
                my_test4.yield_rate = my_test4.yield_rate * (1 - fee)
                with open('btc-test-record-60m.csv', 'a', newline='') as files:
                        mywriter = csv.writer(files)
                        data_to_write = [time(), my_test4.status, my_test4.last_price ,
                                     my_test4.yield_rate, now_price4, my_test4.klines.index_kline.closepriceline[
                                         len(my_test4.klines.index_kline.closepriceline) - 1]]
                        mywriter.writerow(data_to_write)
                my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                            now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test4.status if my_test4.status != None else 0, my_test4.yield_rate,
                my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                my_test4.realtime_yield,
                    now_price4))
            else:
                my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                            now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                        my_test4.status if my_test4.status != None else 0, my_test4.yield_rate,
                        my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                        my_test4.realtime_yield,
                    now_price4))
        elif my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline)-1]>=1 and my_test4.status!=0:
            if my_test4.status==1:
                my_test4.yield_rate=my_test4.yield_rate*(1-fee)*(1+(now_price4-my_test4.last_price)/my_test4.last_price)
                my_test4.status = -1
                my_test4.last_price = now_priceline4[len(now_priceline4)-1]
                my_test4.yield_rate = my_test4.yield_rate * (1 - fee)
                with open('btc-test-record-60m.csv', 'a', newline='') as files:
                        mywriter = csv.writer(files)
                        data_to_write = [time(), my_test4.status, my_test4.last_price ,
                                     my_test4.yield_rate, now_price4, my_test4.klines.index_kline.closepriceline[
                                         len(my_test4.klines.index_kline.closepriceline) - 1]]
                        mywriter.writerow(data_to_write)
                my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                            now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test4.status if my_test4.status != None else 0, my_test4.yield_rate,
                    my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                    my_test4.realtime_yield,
                    now_price4))
            else:
                my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                            now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
                print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test4.status , my_test4.yield_rate,
                    my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                    my_test4.realtime_yield,
                    now_price4))
        elif -1<=my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline)-1]<=1 and my_test4.status!=0:

            my_test4.yield_rate=my_test4.yield_rate*(1-fee)*(1+my_test4.status*(now_price4-my_test4.last_price)/my_test4.last_price) if my_test4.last_price!=0 else my_test4.yield_rate


            my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                        now_price4 - my_test4.last_price) / my_test4.last_price) if my_test4.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
            my_test4.status if my_test4.status != 0 else 0, my_test4.yield_rate,
                my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                my_test4.realtime_yield,
                now_price4))
            my_test4.status = 0
            my_test4.last_price = 0
            with open('btc-test-record-60m.csv', 'a', newline='') as files:
                mywriter = csv.writer(files)
                data_to_write = [time(), my_test4.status, my_test4.last_price ,
                                 my_test4.yield_rate, now_price4, my_test4.klines.index_kline.closepriceline[
                                     len(my_test4.klines.index_kline.closepriceline) - 1]]
                mywriter.writerow(data_to_write)
        else:
            my_test4.realtime_yield = my_test4.yield_rate * (1 + my_test4.status * (
                        now_price4 - my_test4.last_price) / my_test4.last_price)  if my_test4.last_price!=0 else 0
            print("此时的仓位方向为 %d 累计收益率为 %f  指数水平为 %f  实时收益率为%f, 现价为:%f" % (
                my_test4.status if my_test4.status !=0 else 0, my_test4.yield_rate,
                my_test4.klines.index_kline.closepriceline[len(my_test4.klines.index_kline.closepriceline) - 1],
                my_test4.realtime_yield,
                now_price4))
    else:
        print("---------------------------------------------")
        sleep(20)