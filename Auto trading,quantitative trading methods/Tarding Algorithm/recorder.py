import MarcoIndex as MI
import Crawler as cr
import csv
from time import sleep,time
from random import normalvariate
import threading
import os.path
mytimetoad=0.8
dict_timelength={
    '5m':60*3.5,
    '15m':60*14,
    '30m':60*29,
    '60m':60*59,
    '1d':60*60*24-60*3
}

list_yahoo_crypto=[
'BTC-USD',
'ETH-USD',
'XRP-USD',
#'USDT-USD',
'BCH-USD',
'LTC-USD',
'EOS-USD',
'XLM-USD',
'ADA-USD',
'LINK-USD',
'XMR-USD',
'TRX-USD',
'ETC-USD',
'NEO-USD',
'DASH-USD',
'ZEC-USD',
'QTUM-USD',
]

aicoin_crypto_list=[]
for i in list_yahoo_crypto:
    tx=i.find('-')
    aicoin_crypto_list.append(i[:tx])
class wait_and_update(object):
    def __init__(self,interval):
        global dict_timelength
        if interval in dict_timelength:
            self.last_update_time = time()
            self.interval = interval
            self.object_list = []
            self.multiasset_object = MI.klines_multiasset_at_interval(self.interval)
            for i in aicoin_crypto_list:
                sleep(abs(normalvariate(0,abs(mytimetoad))))
                temp_save_i=MI.klines_symbolprice_at_interval(symbol=i, interval=self.interval)
                temp_save_i.update(self.multiasset_object)
                self.object_list.append(temp_save_i)
            threads_list = []
            print("-------------开始更新------------")
            for i in self.object_list:
                threads_list.append(threading.Thread(target=i.update(self.multiasset_object)))
            for k in threads_list:
                sleep(abs(normalvariate(0, abs(mytimetoad))))
                k.start()
            for l in threads_list:
                l.join()
            self.last_update_time = time()
        else:
            raise KeyError('类型错误')
    def update_myself(self):
        global dict_timelength
        if time() - self.last_update_time > dict_timelength[self.interval]:
            threads_list=[]
            print("-------------开始更新------------")
            self.multiasset_object.update()
            for i in self.object_list:
                threads_list.append(threading.Thread(target=i.update(self.multiasset_object)))
            for k in threads_list:
                sleep(abs(normalvariate(0, abs(mytimetoad))))
                k.start()
            for l in threads_list:
                l.join()
            self.last_update_time = time()
        else:
            sleep(15)
            print(-(time() - self.last_update_time - dict_timelength[self.interval]), 's to wait',"-----------------" )

handler_5m=wait_and_update('5m')
print("5m更新完毕")

for i in handler_5m.object_list:
    timestamp = []
    if os.path.exists('E:\evas\marco\save\_5m\symbol-'+i.symbol+'.csv')==True:
        with open('E:\evas\marco\save\_5m\symbol-'+i.symbol+'.csv','r')as read_file:
            a=list(csv.reader(read_file))
            for k in range(0,len(a)):
                timestamp.append(float(a[k][0]))
    with open('E:\evas\marco\save\_5m\symbol-'+i.symbol+'.csv','a',newline='') as myfile_5m:
        writer_5m=csv.writer(myfile_5m)
        for j in range(0,len(i.last_kline.closepriceline)):
            if timestamp!=[]and i.last_kline.timestamp[j]>=max(timestamp):
                print("新增加一个")
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_5m.writerow(send_data)
            elif timestamp!=[] and i.last_kline.timestamp[j]<=max(timestamp):
                pass
            elif timestamp==[]:
                if j== len(i.last_kline.closepriceline)-1:
                    print("船新版本!")
                else:
                    pass
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_5m.writerow(send_data)
            else:
                print("特别情况写入",timestamp,j)
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_5m.writerow(send_data)
sleep(30)

handler_15m=wait_and_update('15m')
print("15m更新完毕")

for i in handler_15m.object_list:
    timestamp = []
    if os.path.exists('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv') == True:
        with open('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv', 'r')as read_file:
            a = list(csv.reader(read_file))
            for k in range(0, len(a)):
                timestamp.append(float(a[k][0]))
    with open('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_15m:
        writer_15m = csv.writer(myfile_15m)
        for j in range(0, len(i.last_kline.closepriceline)):
            if timestamp != [] and i.last_kline.timestamp[j] >= max(timestamp):
                print("新增加一个")
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_15m.writerow(send_data)
            elif timestamp != [] and i.last_kline.timestamp[j] <= max(timestamp):
                pass
            elif timestamp == []:
                if j == len(i.last_kline.closepriceline) - 1:
                    print("船新版本!")
                else:
                    pass
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_15m.writerow(send_data)
            else:
                print("特别情况写入", timestamp, j)
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_15m.writerow(send_data)
sleep(30)

handler_30m=wait_and_update('30m')
print("30m更新完毕")
for i in handler_30m.object_list:
    timestamp = []
    if os.path.exists('E:\evas\marco\save\_30m\symbol-' + i.symbol + '.csv') == True:
        with open('E:\evas\marco\save\_30m\symbol-' + i.symbol + '.csv', 'r')as read_file:
            a = list(csv.reader(read_file))
            for k in range(0, len(a)):
                timestamp.append(float(a[k][0]))
    with open('E:\evas\marco\save\_30m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_30m:
        writer_30m = csv.writer(myfile_30m)
        for j in range(0, len(i.last_kline.closepriceline)):
            if timestamp != [] and i.last_kline.timestamp[j] >= max(timestamp):
                print("新增加一个")
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_30m.writerow(send_data)
            elif timestamp != [] and i.last_kline.timestamp[j] <= max(timestamp):
                pass
            elif timestamp == []:
                if j == len(i.last_kline.closepriceline) - 1:
                    print("船新版本!")
                else:
                    pass
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_30m.writerow(send_data)
            else:
                print("特别情况写入", timestamp, j)
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_30m.writerow(send_data)
sleep(30)

handler_60m=wait_and_update('60m')
print("60m更新完毕")
for i in handler_60m.object_list:
    timestamp = []
    if os.path.exists('E:\evas\marco\save\_60m\symbol-' + i.symbol + '.csv') == True:
        with open('E:\evas\marco\save\_60m\symbol-' + i.symbol + '.csv', 'r')as read_file:
            a = list(csv.reader(read_file))
            for k in range(0, len(a)):
                timestamp.append(float(a[k][0]))
    with open('E:\evas\marco\save\_60m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_60m:
        writer_60m = csv.writer(myfile_60m)
        for j in range(0, len(i.last_kline.closepriceline)):
            if timestamp != [] and i.last_kline.timestamp[j] >= max(timestamp):
                print("新增加一个")
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_60m.writerow(send_data)
            elif timestamp != [] and i.last_kline.timestamp[j] <= max(timestamp):
                pass
            elif timestamp == []:
                if j == len(i.last_kline.closepriceline) - 1:
                    print("船新版本!")
                else:
                    pass
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_60m.writerow(send_data)
            else:
                print("特别情况写入", timestamp, j)
                send_data = [i.last_kline.timestamp[j], i.last_kline.openpriceline[j], i.last_kline.closepriceline[j],
                             i.last_kline.highpriceline[j], i.last_kline.lowpriceline[j],
                             i.index_kline.openpriceline[j], i.index_kline.closepriceline[j],
                             i.index_kline.highpriceline[j], i.index_kline.lowpriceline[j]]
                writer_60m.writerow(send_data)
sleep(30)

while True:
    if time()- handler_5m.last_update_time > dict_timelength[handler_5m.interval]:
        print("更新5分钟的时间到了")
        handler_5m.update_myself()
        for i in handler_5m.object_list:
            with open('E:\evas\marco\save\_5m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_5m:
                writer_5m = csv.writer(myfile_5m)
                send_data = [i.last_kline.timestamp[len(i.last_kline.timestamp)-1],i.last_kline.openpriceline[len(i.last_kline.openpriceline)-1], i.last_kline.closepriceline[len(i.last_kline.closepriceline)-1],
                                 i.last_kline.highpriceline[len(i.last_kline.highpriceline)-1], i.last_kline.lowpriceline[len(i.last_kline.lowpriceline)-1],
                                 i.index_kline.openpriceline[len(i.last_kline.openpriceline)-1], i.index_kline.closepriceline[len(i.last_kline.closepriceline)-1],
                                 i.index_kline.highpriceline[len(i.last_kline.highpriceline)-1], i.index_kline.lowpriceline[len(i.last_kline.lowpriceline)-1]]
                writer_5m.writerow(send_data)
    elif time()- handler_15m.last_update_time > dict_timelength[handler_15m.interval]:
        print("更新15分钟的时间到了")
        handler_15m.update_myself()
        for i in handler_15m.object_list:
            with open('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_15m:
                writer_15m = csv.writer(myfile_15m)
                send_data = [i.last_kline.timestamp[len(i.last_kline.timestamp)-1],i.last_kline.openpriceline[len(i.last_kline.openpriceline) - 1],
                             i.last_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.last_kline.highpriceline[len(i.last_kline.highpriceline)-1],
                             i.last_kline.lowpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.openpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.highpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.lowpriceline[len(i.last_kline.closepriceline) - 1]]
                writer_15m.writerow(send_data)
    elif time()- handler_30m.last_update_time > dict_timelength[handler_30m.interval]:
        print("更新30分钟的时间到了")
        handler_30m.update_myself()
        for i in handler_30m.object_list:
            with open('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_30m:
                writer_30m = csv.writer(myfile_30m)
                send_data = [i.last_kline.timestamp[len(i.last_kline.timestamp)-1],i.last_kline.openpriceline[len(i.last_kline.openpriceline) - 1],
                             i.last_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.last_kline.highpriceline[len(i.last_kline.highpriceline)-1],
                             i.last_kline.lowpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.openpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.highpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.lowpriceline[len(i.last_kline.closepriceline) - 1]]
                writer_30m.writerow(send_data)
    elif time()-handler_60m.last_update_time > dict_timelength[handler_60m.interval]:
        print("更新60分钟的时间到了")
        handler_60m.update_myself()
        for i in handler_60m.object_list:
            with open('E:\evas\marco\save\_15m\symbol-' + i.symbol + '.csv', 'a', newline='') as myfile_60m:
                writer_60m = csv.writer(myfile_60m)
                send_data = [i.last_kline.timestamp[len(i.last_kline.timestamp)-1],i.last_kline.openpriceline[len(i.last_kline.openpriceline) - 1],
                             i.last_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.last_kline.highpriceline[len(i.last_kline.highpriceline)-1],
                             i.last_kline.lowpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.openpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.closepriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.highpriceline[len(i.last_kline.closepriceline) - 1],
                             i.index_kline.lowpriceline[len(i.last_kline.closepriceline) - 1]]
                writer_60m.writerow(send_data)
    else:
        pass

