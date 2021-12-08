
import Crawler as cr
import DataProcess as dp
import numpy as np
import time
import matplotlib.pyplot as mat
from requests import get,post
from json import loads,dumps
from random import normalvariate,uniform
from statsmodels.api import OLS
from statsmodels.api import add_constant
from sklearn.decomposition import PCA
from csv import writer
timetoad=1

dict_timegap={
    '5m':5*60,
    '15m':15*60,
    '30m':30*60,
    '60m':60*60,
    '1d':60*60*24
}

dict_timepoint_at_interval={
    '5m':None,
    '15m':None,
    '30m':None,
    '60m':None,
    '70m':None
}

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

class klines_multiasset_at_interval(object):
    def __init__(self,interval,dataset_kind='quick'):
        self.interval=interval
        self.dataset_kind=dataset_kind
        self.klines=Get_multiasset_data(self.interval,dataset_kind=self.dataset_kind).copy()
        self.last_update=time.time()
        self.previous_yield=None

    def update(self):
        self.klines = Get_multiasset_data(self.interval,  dataset_kind=self.dataset_kind).copy()
        self.previous_yield=np.mean(self.klines[2].closepriceline)
        self.last_update=time.time()
        print("更新 %s 周期 完毕"%self.interval)
class klines_symbolprice_at_interval(object):
    def __init__(self,symbol,interval,dataset_kind='quick'):
        self.symbol=symbol
        self.interval=interval
        self.dataset_kind='quick'
        self.multiasset_data=None
        self.index_kline=kline()
        self.last_kline=kline()
        self.yield_ols_result=None
        self.APT_alpha=None
        self.APT_beta=None
        self.score=None
    def update(self,klines_multiasset_at_interval_klines):
        self.multiasset_data=klines_multiasset_at_interval_klines.klines
        if self.symbol in aicoin_crypto_list:
            symbol_kline = cr.realtime_klineprice_aicoin(self.symbol,self.interval)
            symbol_kline.closepriceline=dp.linear_adjust(symbol_kline.closepriceline)
            symbol_kline.highpriceline = dp.linear_adjust(symbol_kline.highpriceline)
            symbol_kline.lowpriceline = dp.linear_adjust(symbol_kline.lowpriceline)
            symbol_kline.openpriceline = dp.linear_adjust(symbol_kline.openpriceline)
            dict_dataset_kind = {
                'quick': cr.dict_quick_list_yahoo,
                'normal:': cr.dict_normal_list_yahoo,
                'all': cr.dict_all_list_yahoo
            }
            if self.dataset_kind in dict_dataset_kind:
                symbol_kline.closepriceline, self.multiasset_data[0].closepriceline=dp.timeserieslength_adjust([symbol_kline.closepriceline,self.multiasset_data[0].closepriceline])
                ols_params_close=OLS(symbol_kline.closepriceline,self.multiasset_data[0].closepriceline).fit().params[0]
                temp_list_close=[symbol_kline.closepriceline[i]/self.multiasset_data[0].closepriceline[i]-ols_params_close for i in range(0,len(symbol_kline.closepriceline))]
                temp_std_close=np.std(temp_list_close)
                normal_close=dp.normalize(symbol_kline.closepriceline)
                self.index_kline.closepriceline=[temp_list_close[i]/temp_std_close-normal_close[i] for i in range(0,len(normal_close))]

                symbol_kline.openpriceline, self.multiasset_data[0].openpriceline = dp.timeserieslength_adjust(
                    [symbol_kline.openpriceline, self.multiasset_data[0].openpriceline])
                ols_params_open = \
                OLS(symbol_kline.openpriceline, self.multiasset_data[0].openpriceline).fit().params[0]
                temp_list_open = [
                    symbol_kline.openpriceline[i] / self.multiasset_data[0].openpriceline[i] - ols_params_open for i
                    in range(0, len(symbol_kline.openpriceline))]
                temp_std_open = np.std(temp_list_open)
                normal_open = dp.normalize(symbol_kline.openpriceline)
                self.index_kline.openpriceline = [temp_list_open[i] / temp_std_open - normal_open[i] for i in
                                                   range(0, len(normal_open))]

                symbol_kline.highpriceline, self.multiasset_data[0].highpriceline = dp.timeserieslength_adjust(
                    [symbol_kline.highpriceline, self.multiasset_data[0].highpriceline])
                ols_params_high = \
                    OLS(symbol_kline.highpriceline, self.multiasset_data[0].highpriceline).fit().params[0]
                temp_list_high = [
                    symbol_kline.highpriceline[i] / self.multiasset_data[0].highpriceline[i] - ols_params_high for i
                    in range(0, len(symbol_kline.highpriceline))]
                temp_std_high = np.std(temp_list_high)
                normal_high = dp.normalize(symbol_kline.highpriceline)
                self.index_kline.highpriceline = [temp_list_high[i] / temp_std_high - normal_high[i] for i in
                                                  range(0, len(normal_high))]

                symbol_kline.lowpriceline, self.multiasset_data[0].lowpriceline = dp.timeserieslength_adjust(
                    [symbol_kline.lowpriceline, self.multiasset_data[0].lowpriceline])
                ols_params_low = \
                    OLS(symbol_kline.lowpriceline, self.multiasset_data[0].lowpriceline).fit().params[0]
                temp_list_low = [
                    symbol_kline.lowpriceline[i] / self.multiasset_data[0].lowpriceline[i] - ols_params_low for i
                    in range(0, len(symbol_kline.lowpriceline))]
                temp_std_low = np.std(temp_list_low)
                normal_low = dp.normalize(symbol_kline.highpriceline)
                self.index_kline.lowpriceline = [temp_list_low[i] / temp_std_low - normal_low[i] for i in
                                                  range(0, len(normal_low))]
                self.index_kline.timestamp=symbol_kline.timestamp
                self.index_kline.timestamptostr()
                self.index_kline.openpriceline,self.index_kline.closepriceline,self.index_kline.highpriceline,self.index_kline.lowpriceline,self.index_kline.timestamp,self.index_kline.str_timestamp=\
                dp.timeserieslength_adjust([self.index_kline.openpriceline,self.index_kline.closepriceline,self.index_kline.highpriceline,self.index_kline.lowpriceline,self.index_kline.timestamp,self.index_kline.str_timestamp])
                self.index_kline.self_lengthadjust()

                symbol_kline.timestamptostr()
                marco_yield=self.multiasset_data[2].closepriceline
                close_yield=dp.diff_ratio(symbol_kline.closepriceline)
                yield_ols_result=OLS(close_yield,add_constant(marco_yield)).fit()
                print(self.symbol,"+",self.interval,"更新完毕",self.APT_alpha-yield_ols_result.params[0] if self.APT_alpha!=None else 0,self.APT_beta-yield_ols_result.params[1] if self.APT_beta!=None else 0)
                self.APT_alpha=yield_ols_result.params[0]
                self.APT_beta=yield_ols_result.params[1]
                self.yield_ols_result=OLS(close_yield,add_constant(marco_yield)).fit()
                self.last_kline=symbol_kline
                self.last_kline.timestamptostr()
                self.score=self.APT_alpha+self.APT_beta*np.mean(self.multiasset_data[2].closepriceline)
            else:
                return None
        else:
            return None
list_yahoo_crypto=[
'BTC-USD',
'ETH-USD',
'XRP-USD',
'USDT-USD',
'BCH-USD',
'LTC-USD',
'BNB-USD',
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
'STRAT-USD',
'RLC-USD',
'BTCD-USD',
'ARK-USD',
'GNO-USD',
'BNT-USD',
'MTL-USD',
'WTC-USD',
'ICN-USD',
'FUN-USD',
'FCT-USD',
'PIVX-USD',
'PPT-USD',
'VTC-USD',
'GBYTE-USD',
'STORJ-USD',
'VERI-USD',
'CVC-USD',
'SYS-USD',
'GAS-USD',
'NXT-USD',
'QASH-USD',
'DGD-USD',
'NXS-USD',
'BLOCK-USD',
'ETP-USD',
'KIN-USD',
'NAV-USD',
'NEBL-USD',
'PAY-USD',
'PART-USD',
'SALT-USD',
'ADX-USD',
'VGX-USD',
'ETHOS-USD',
'QRL-USD',
'SMART-USD',
'SNGLS-USD',
'UBQ-USD',
'MLN-USD',
'TAAS-USD',
'LKK-USD',
'DCN-USD',
'GAME-USD',
'XCP-USD',
'DNT-USD',
'SNM-USD',
'WINGS-USD',
'IOC-USD',
'FAIR-USD',
'SUB-USD',
'MGO-USD',
'EDG-USD',
'NLC2-USD',
'BTM1-USD',
'MCAP-USD',
'ATB-USD',
'FRST-USD',
'XUC-USD'
]
aicoin_crypto_list=[]
for i in list_yahoo_crypto:
    tx=i.find('-')
    aicoin_crypto_list.append(i[:tx])
def Getrealtime_kline_from_symbol(interval,symbol):
    kline_result = cr.get_timeseries_result_yahoo(kind=symbol+'-USD', interval=interval)
    if kline_result!=None:
        one_kline = kline()
        for l in range(0, len(kline_result[0])):
            one_kline.lowpriceline.append(kline_result[1][l][0])
            one_kline.highpriceline.append(kline_result[1][l][1])
            one_kline.openpriceline.append(kline_result[1][l][2])
            one_kline.closepriceline.append(kline_result[1][l][3])
            one_kline.timestamp.append(kline_result[0][l])
            one_kline.volume.append(kline_result[1][l][4])
        one_kline.self_lengthadjust()
        return one_kline
    else:
        print("None")
        return None
def Get_multiasset_data_from_timeseries_singleline(data):
    data=dp.timeserieslength_adjust(data)
    array_timeseries = np.array(dp.timeserieslength_adjust(data)).T
    marco_line = dp.panaldata_mean(data)
    pca = PCA(n_components=1)
    pca_line = [i[0] for i in pca.fit_transform(array_timeseries)]
    for i in range(0,len(data)):
        data[i]=dp.diff_ratio(data[i])
    marco_line_yield= dp.panaldata_mean(data)
    pca_yield = PCA(n_components=1)
    pca_line_yield = [i[0] for i in pca_yield.fit_transform(np.array(dp.timeserieslength_adjust(data)).T)]
    pca_line_yield, marco_line_yield = dp.timeserieslength_adjust([pca_line_yield, marco_line_yield])
    pca_line, marco_line = dp.timeserieslength_adjust([pca_line, marco_line])
    return [marco_line, pca_line,marco_line_yield,pca_line_yield]

def Get_multiasset_data(interval,dataset_kind='quick'):
    counts = 0
    kline_list = []

    dict_dataset_kind = {
        'quick': cr.dict_quick_list_yahoo,
        'normal:': cr.dict_normal_list_yahoo,
        'all': cr.dict_all_list_yahoo
    }
    if dataset_kind in dict_dataset_kind:
        one_kline = kline()
        for i in dict_dataset_kind[dataset_kind]:
            one_kline = kline()
            timetowait = abs(normalvariate(0, timetoad))
            time.sleep(timetowait)
            kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
            if kline_result == []:
                continue
            else:
                for l in range(0, len(kline_result[0])):
                    one_kline.lowpriceline.append(kline_result[1][l][0])
                    one_kline.highpriceline.append(kline_result[1][l][1])
                    one_kline.openpriceline.append(kline_result[1][l][2])
                    one_kline.closepriceline.append(kline_result[1][l][3])
                    one_kline.timestamp.append(kline_result[0][l])
                    one_kline.volume.append(kline_result[1][l][4])
                one_kline.lowpriceline = dp.linear_adjust(one_kline.lowpriceline)
                one_kline.highpriceline = dp.linear_adjust(one_kline.highpriceline)
                one_kline.openpriceline = dp.linear_adjust(one_kline.openpriceline)
                one_kline.closepriceline = dp.linear_adjust(one_kline.closepriceline)
                one_kline.timestamp = dp.linear_adjust(one_kline.timestamp)
                one_kline.timestamptostr()
                one_kline.volume = dp.linear_adjust(one_kline.volume)
                one_kline.self_lengthadjust()
            counts+=1
            print("%s finished %f percent" % (i, counts * 100 / len(dict_dataset_kind[dataset_kind])))
            if len(one_kline.closepriceline)>=50:
                kline_list.append(one_kline)
        if kline_list != None:

            lowprice_timeseries = [i.lowpriceline for i in kline_list]
            highprice_timeseries = [i.highpriceline for i in kline_list]
            openprice_timeseries = [i.openpriceline for i in kline_list]
            closeprice_timeseries = [i.closepriceline for i in kline_list]


            marco_kline = kline()
            pca_kline = kline()
            marco_kline_yield=kline()
            pca_kline_yield=kline()

            result_lowprice = Get_multiasset_data_from_timeseries_singleline(lowprice_timeseries)
            result_highprice = Get_multiasset_data_from_timeseries_singleline(highprice_timeseries)
            result_closeprice = Get_multiasset_data_from_timeseries_singleline(closeprice_timeseries)
            result_openprice = Get_multiasset_data_from_timeseries_singleline(openprice_timeseries)

            marco_kline.lowpriceline = result_lowprice[0]
            pca_kline.lowpriceline = result_lowprice[1]
            marco_kline_yield.lowpriceline=result_lowprice[2]
            pca_kline_yield.lowpriceline=result_lowprice[3]

            marco_kline.highpriceline = result_highprice[0]
            pca_kline.highpriceline = result_highprice[1]
            marco_kline_yield.highpriceline = result_highprice[2]
            pca_kline_yield.highpriceline = result_highprice[3]

            marco_kline.openpriceline = result_openprice[0]
            pca_kline.openpriceline = result_openprice[1]
            marco_kline_yield.openpriceline = result_openprice[2]
            pca_kline_yield.openpriceline = result_openprice[3]

            marco_kline.closepriceline = result_closeprice[0]
            pca_kline.closepriceline = result_closeprice[1]
            marco_kline_yield.closepriceline = result_closeprice[2]
            pca_kline_yield.closepriceline = result_closeprice[3]

            marco_kline.timestamp = marco_kline.timestamp[
                                    len(marco_kline.timestamp) - len(marco_kline.closepriceline):len(marco_kline.timestamp)]
            marco_kline.timestamptostr()

            pca_kline.timestamp = pca_kline.timestamp[len(pca_kline.timestamp) - len(pca_kline.closepriceline):len(pca_kline.timestamp)]
            pca_kline.timestamptostr()

            marco_kline_yield.timestamp = marco_kline_yield.timestamp[
                                    len(marco_kline_yield.timestamp) - len(marco_kline_yield.closepriceline):len(
                                        marco_kline_yield.timestamp)]
            marco_kline_yield.timestamptostr()

            pca_kline_yield.timestamp = pca_kline_yield.timestamp[
                                    len(pca_kline_yield.timestamp) - len(pca_kline_yield.closepriceline):len(
                                        pca_kline_yield.timestamp)]
            pca_kline_yield.timestamptostr()

            for i in range(0, len(marco_kline.closepriceline)):
                if marco_kline.highpriceline[i] < marco_kline.lowpriceline[i]:
                    p = marco_kline.highpriceline[i]
                    marco_kline.highpriceline[i] = marco_kline.lowpriceline[i]
                    marco_kline.lowpriceline[i] = p

            for i in range(0, len(pca_kline.closepriceline)):
                if pca_kline.highpriceline[i] < pca_kline.lowpriceline[i]:
                    p = pca_kline.highpriceline[i]
                    pca_kline.highpriceline[i] = pca_kline.lowpriceline[i]
                    pca_kline.lowpriceline[i] = p

            for i in range(0, len(marco_kline_yield.closepriceline)):
                if marco_kline_yield.highpriceline[i] < marco_kline_yield.lowpriceline[i]:
                    p = marco_kline_yield.highpriceline[i]
                    marco_kline_yield.highpriceline[i] = marco_kline_yield.lowpriceline[i]
                    marco_kline_yield.lowpriceline[i] = p

            for i in range(0, len(pca_kline_yield.closepriceline)):
                if pca_kline_yield.highpriceline[i] < pca_kline_yield.lowpriceline[i]:
                    p = pca_kline_yield.highpriceline[i]
                    pca_kline_yield.highpriceline[i] = pca_kline_yield.lowpriceline[i]
                    pca_kline_yield.lowpriceline[i] = p



            return [marco_kline, pca_kline,marco_kline_yield,pca_kline_yield]
        else:
            print("获取失败")
            return None
    else:
        print("Not in dict")
        return None

def Getindics_and_PCA_from_timeseries_singleline(data,symbol_kline,type,not_yield=True):
    array_timeseries = np.array(dp.timeserieslength_adjust(data))
    type_list = {
        'open':symbol_kline.openpriceline,
        'close':symbol_kline.closepriceline,
        'low':symbol_kline.lowpriceline,
        'high':symbol_kline.highpriceline,
    }
    if not_yield==True:
        if type in type_list:
            main_line = type_list[type]
            main_line = dp.linear_adjust(main_line)
            marco_line = dp.panaldata_mean(data)
            pca = PCA(n_components=1)
            pca_line = [i[0] for i in pca.fit_transform(array_timeseries)]
            main_line, pca_line, marco_line = dp.timeserieslength_adjust([main_line, pca_line, marco_line])
            ols_result = OLS(main_line, marco_line).fit()
            print(np.cov(marco_line,main_line)[0][1]/(np.std(marco_line)*np.std(main_line)))
            gap_list = [main_line[k] / marco_line[k] - ols_result.params[0] for k in range(0, len(main_line))]
            std_param = np.std(gap_list)
            previous_index_line = [(main_line[i] / marco_line[i] - ols_result.params[0]) / std_param for i in
                                   range(0, len(marco_line))]
            normal_line = dp.normalize(main_line)
            return [[previous_index_line[k] - normal_line[k] for k in range(0, len(previous_index_line))], pca_line,
                    marco_line, normal_line,main_line,ols_result]
    else:
        if type in type_list:
            main_line = type_list[type]
            main_line = dp.diff_ratio(dp.linear_adjust(main_line))
            marco_line = dp.diff_ratio(dp.panaldata_mean(data))
            pca = PCA(n_components=1)
            pca_line =dp.diff_ratio([i[0] for i in pca.fit_transform(array_timeseries)])
            main_line, pca_line, marco_line = dp.timeserieslength_adjust([main_line, pca_line, marco_line])
            ols_result = OLS(main_line, marco_line).fit()
            gap_list = [main_line[k] / marco_line[k] - ols_result.params[0] for k in range(0, len(main_line))]
            std_param = np.std(gap_list)
            previous_index_line = [(main_line[i] / marco_line[i] - ols_result.params[0]) / std_param for i in
                                   range(0, len(marco_line))]
            normal_line = dp.normalize(main_line)
            return [[previous_index_line[k] - normal_line[k] for k in range(0, len(previous_index_line))],pca_line,
                    marco_line, normal_line,main_line,ols_result]

def Get_index_kline(interval,symbol,dataset_kind='quick',not_yield=True):
    symbol_kline=Getrealtime_kline_from_symbol(interval,symbol)
    if symbol in aicoin_crypto_list:
        counts = 0
        kline_list = []
        dict_dataset_kind = {
            'quick': cr.dict_quick_list_yahoo,
            'normal': cr.dict_normal_list_yahoo,
            'all': cr.dict_all_list_yahoo
        }
        if dataset_kind in dict_dataset_kind:
            one_kline=kline()
            for i in dict_dataset_kind[dataset_kind]:
                one_kline = kline()
                timetowait = abs(normalvariate(0,timetoad))
                time.sleep(timetowait)
                kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
                if kline_result == []:
                    continue
                else:
                    for l in range(0, len(kline_result[0])):
                        one_kline.lowpriceline.append(kline_result[1][l][0])
                        one_kline.highpriceline.append(kline_result[1][l][1])
                        one_kline.openpriceline.append(kline_result[1][l][2])
                        one_kline.closepriceline.append(kline_result[1][l][3])
                        one_kline.timestamp.append(kline_result[0][l])
                        one_kline.volume.append(kline_result[1][l][4])
                    one_kline.lowpriceline = dp.linear_adjust(one_kline.lowpriceline)
                    one_kline.highpriceline = dp.linear_adjust(one_kline.highpriceline)
                    one_kline.openpriceline = dp.linear_adjust(one_kline.openpriceline)
                    one_kline.closepriceline = dp.linear_adjust(one_kline.closepriceline)
                    one_kline.timestamp = dp.linear_adjust(one_kline.timestamp)
                    one_kline.timestamptostr()
                    one_kline.volume = dp.linear_adjust(one_kline.volume)
                    one_kline.self_lengthadjust()
                    counts += 1
                print("%s finished %f percent"%(i,counts*100/len(dict_dataset_kind[dataset_kind])))
                if len(one_kline.closepriceline)>50:
                    kline_list.append(one_kline)
            if kline_list != None:
                lowprice_timeseries = [i.lowpriceline for i in kline_list]
                highprice_timeseries = [i.highpriceline for i in kline_list]
                openprice_timeseries = [i.openpriceline for i in kline_list]
                closeprice_timeseries = [i.closepriceline for i in kline_list]
                index_kline = kline()
                marco_kline=kline()
                pca_kline=kline()

                result_lowprice=Getindics_and_PCA_from_timeseries_singleline(lowprice_timeseries,symbol_kline=symbol_kline, type='low',
                                                      not_yield=not_yield)
                result_highprice = Getindics_and_PCA_from_timeseries_singleline(highprice_timeseries,
                                                                               symbol_kline=symbol_kline, type='high',
                                                                               not_yield=not_yield)
                result_closeprice = Getindics_and_PCA_from_timeseries_singleline(closeprice_timeseries,
                                                                               symbol_kline=symbol_kline, type='close',
                                                                               not_yield=not_yield)
                result_openprice = Getindics_and_PCA_from_timeseries_singleline(openprice_timeseries,
                                                                               symbol_kline=symbol_kline, type='open',
                                                                               not_yield=not_yield)

                index_kline.lowpriceline =result_lowprice[0]
                marco_kline.lowpriceline=result_lowprice[2]
                pca_kline.lowpriceline=result_lowprice[1]

                index_kline.highpriceline = result_highprice[0]
                marco_kline.highpriceline = result_highprice[2]
                pca_kline.highpriceline = result_highprice[1]

                index_kline.openpriceline = result_openprice[0]
                marco_kline.openpriceline = result_openprice[2]
                pca_kline.openpriceline = result_openprice[1]

                index_kline.closepriceline = result_closeprice[0]
                marco_kline.closepriceline = result_closeprice[2]
                pca_kline.closepriceline = result_closeprice[1]

                volume = symbol_kline.volume
                index_kline.volume = volume[len(volume) - len(index_kline.closepriceline):len(volume)]

                timestamp = symbol_kline.timestamp
                index_kline.timestamp = timestamp[len(timestamp) - len(index_kline.closepriceline):len(timestamp)]
                index_kline.timestamptostr()
                marco_kline.timestamp = timestamp[len(timestamp) - len(marco_kline.closepriceline):len(timestamp)]
                marco_kline.timestamptostr()
                pca_kline.timestamp = timestamp[len(timestamp) - len(pca_kline.closepriceline):len(timestamp)]
                pca_kline.timestamptostr()
                for i in range(0, len(index_kline.closepriceline)):
                    if index_kline.highpriceline[i] < index_kline.lowpriceline[i]:
                        p = index_kline.highpriceline[i]
                        index_kline.highpriceline[i] = index_kline.lowpriceline[i]
                        index_kline.lowpriceline[i] = p

                index_kline.self_lengthadjust()
                marco_kline.self_lengthadjust()
                pca_kline.self_lengthadjust()

                return [index_kline,marco_kline,pca_kline]
            else:
                print("获取失败")
                return None
        else:
            print("Not in dict")
            return None
    else:
        print("Not in list")
        return None

def Get_index_close(interval,symbol,dataset_kind='quick'):
    return Get_index_kline(interval,symbol,dataset_kind)[0].closepriceline

def Get_index_close_yield(interval,symbol,dataset_kind='quick'):
    return Get_index_kline(interval, symbol, dataset_kind,not_yield=False)[0].closepriceline

def APT_BTC_to_Marcofactor_contineous(interval,symbol,dataset_type='quick'):
    get_kline_result=Get_index_kline(interval, symbol, dataset_type,not_yield=False)
    main_line=get_kline_result[0].closepriceline
    marco_line=get_kline_result[1].closepriceline
    new_xline=add_constant(marco_line)
    no=get_kline_result[2].closepriceline
    ols_result=OLS(main_line,new_xline).fit()
    return [ols_result.params[0],ols_result.params[1],ols_result]

def CAPM_choiced_to_Cryptocurrencies_index_contineous(choicedtrade,interval):
    
    return []

aa=Get_index_kline('15m','BTC','normal')
print("dfgsdfgsdf")
print("sfsdf")