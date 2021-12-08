from MarcoIndex import kline
from DataProcess import check_nulllist,EMA,timeserieslength_adjust,diff_ratio,max_min,check_constant,check_timeseries, check_max_list,check_zero_list,check_all_zero_list
from Crawler import realtime_klineprice_aicoin,realtime_klineprice_aicoin_bysymbol,get_all_crptocurrency_list
from statsmodels.api import OLS,add_constant
from math import log
from csv import reader
from random import normalvariate
from time import sleep,time
from numpy import max,min,mean,std,inf,sum
from sys import exc_info

'''
初始草稿版本
'''
test_symbol_list=[
'btcusdt:huobipro',
'bchabcbtc:okex',
'ethbtc:okex',
'bchsvbtc:okex',
'eosbtc:okex',
'okbbtc:okex',
'btmbtc:okex',
'ltcbtc:okex'
'lrcbtc:okex'
'xrpbtc:okex'
'omgbtc:okex',
'neobtc:okex'
'etcbtc:okex'
'qtumbtc:okex',
'zilbtc:okex',
'xlmbtc:okex',
'gasbtc:okex',
'adabtc:okex',
'iostbtc:okex',
'mkrbtc:okex',
'zrxbtc:okex',
'arkbtc:okex',
'linkbtc:okex',
'elfbtc:okex',
'paybtc:okex',
'trxbtc:okex',
'hbarbtc:okex',
'nanobtc:okex',
'ontbtc:okex',
'manabtc:okex',
'zecbtc:okex',
'algobtc:okex',
'vsysbtc:okex',
'mdtbtc:okex',
'scbtc:okex',
'abtbtc:okex',
'sbtcbtc:okex',
'ardrbtc:okex',
'dgbbtc:okex',
'cvtbtc:okex',
'gnxbtc:okex',
'kncbtc:okex',
'gusdbtc:okex',
'crobtc:okex',
'atombtc:okex',
'mithbtc:okex',
'thetabtc:okex',
'hycbtc:okex',
'egtbtc:okex',
'iotabtc:okex',
'bhpbtc:okex',
'bcdbtc:okex',
'dashbtc:okex',
'zenbtc:okex',
'intbtc:okex',
'swftcbtc:okex',
'hsrbtc:okex',
'xtzbtc:okex',
'kcashbtc:okex',
'wxtbtc:okex',
'xembtc:okex',
'icxbtc:okex',
'sntbtc:okex',
'bntbtc:okex',
'nasbtc:okex',
'tctbtc:okex',
'actbtc:okex',
'oxtbtc:okex',
'paxbtc:okex',
'dnabtc:okex',
'cvcbtc:okex',
'cmtbtc:okex',
'bttbtc:okex',
'btgbtc:okex',
'gtobtc:okex',
'aacbtc:okex',
'mofbtc:okex',
'aebtc:okex',
'batbtc:okex',
'itcbtc:okex',
'vitebtc:okex',
'orsbtc:okex',
'spndbtc:okex',
'truebtc:okex',
'xmrbtc:okex',
'ctcbtc:okex',
'letbtc:okex',
'wavesbtc:okex',
'yoyobtc:okex',
'tusdbtc:okex',
'nulsbtc:okex',
'bcxbtc:okex',
'wtcbtc:okex',
'chatbtc:okex',
'socbtc:okex',
'ctxcbtc:okex',
'dcrbtc:okex',
'pstbtc:okex',
'triobtc:okex',
'lskbtc:okex',
'lbabtc:okex',
'vibbtc:okex',
'mcobtc:okex',
'gntbtc:okex',
'edobtc:okex',
'kanbtc:okex',
'qunbtc:okex',
'rvnbtc:okex',
'funbtc:okex',
'leobtc:okex',
'pmabtc:okex',
'sncbtc:okex',
'usdcbtc:okex',
'youbtc:okex',
'apmbtc:okex'
]
timetoad=3
fee_rate=0.0005
dict_timelength_yearly = {
    '1m': 1 / (365 * 24 * 60),
    '3m': 1 / (365 * 24 * 20),
    '5m': 1 / (365 * 24 * 12),
    '10m': 1 / (365 * 24 * 6),
    '15m': 1 / (365 * 24 * 4),
    '30m': 1 / (365 * 24 * 2),
    '1h': 1 / (365 * 24),
    '2h': 1 / (365 * 12),
    '3h': 1 / (365 * 8),
    '4h': 1 / (365 * 6),
    '6h': 1 / (365 * 12),
    '12h': 1 / (365 * 2),
    '1d': 1 / (365),
    '2d': 2 / (365),
    '3d': 3 / (365),
    '5d': 5 / (365),
    '1w': 7 / (365),
}





dict_interval={#测试阶段，暂时使用这些周期，正式使用再将注释去掉。
    #'1m': 1 ,
    #'3m':3,
    '5m': 5,
    #'10m': 10,
    '15m': 15,
    #'30m': 30,
    '1h': 60,
    #'2h': 120,
    #'3h': 180,
    #'4h': 240,
    '6h': 360,
    #'12h': 720,
    '1d': 1440,
    #'2d': 2880,
    #'3d': 4320,
    #'5d': 7200,
    #'1w': 10080,
}

standard_save={
    'symbol':None,
    'interval':None,
    'profit_rate':None,
    'yearly_yield':None,
    'cal_timelength_yearly':None
}
def yield_yearly(profit_rate):#年化收益率计算
    global dict_timelength_yearly
    return float(log(1+profit_rate)) if 1+profit_rate>0 else -1
def yield_to_maxloss_yearly(position_list,price_list):#最大回撤
    diff_ratio_data = diff_ratio(price_list)
    position_list, diff_ratio_data = timeserieslength_adjust([position_list, diff_ratio_data])
    profitrate = 1
    profitrateline=[]
    cal = False
    for i in range(0, len(diff_ratio_data)):
        profitrateline.append(position_list[i] * diff_ratio_data[i])
        if position_list[i] == 1:
            if cal == True:
                profitrate = profitrate * (1 + diff_ratio_data[i])

            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
        elif position_list[i] == 0:
            if cal == True:
                profitrate = profitrate * (1 - fee_rate)
            else:
                pass
        else:
            if cal == True:
                profitrate = profitrate * (1 - diff_ratio_data[i])
            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
    return min(profitrateline)

def yield_to_stdunit(position_list,price_list):#夏普比率，设定无风险利率为0
    diff_ratio_data = diff_ratio(price_list)
    position_list, diff_ratio_data = timeserieslength_adjust([position_list, diff_ratio_data])
    profitrate = 1
    profitrateline = []
    cal = False
    for i in range(0, len(diff_ratio_data)):
        profitrateline.append(position_list[i] * diff_ratio_data[i])
        if position_list[i] == 1:
            if cal == True:
                profitrate = profitrate * (1 + diff_ratio_data[i])

            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
        elif position_list[i] == 0:
            if cal == True:
                profitrate = profitrate * (1 - fee_rate)
            else:
                pass
        else:
            if cal == True:
                profitrate = profitrate * (1 - diff_ratio_data[i])
            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
    return (float(log(1 + profitrate)) if 1 + profitrate > 0 else -1) / std(profitrateline) if check_all_zero_list(profitrateline)!=True else 1

def profit_rate_cal(position_list,price_list):#在当前数据长度下，比如5分钟k线，共500个数据，就是一天左右的该指标下的收益率
    diff_ratio_data=diff_ratio(price_list)
    position_list,diff_ratio_data=timeserieslength_adjust([position_list,diff_ratio_data])
    profitrate=1
    cal=False
    for i in range(0,len(diff_ratio_data)):
        if position_list[i]==1:
            if cal==True:
                profitrate = profitrate *(1+diff_ratio_data[i])
            else:
                profitrate=profitrate*(1-fee_rate)
            cal=True
        elif position_list[i]==0:
            if cal==True:
                profitrate = profitrate * (1 - fee_rate)
            else:
                pass
        else:
            if cal==True:
                profitrate = profitrate *(1-diff_ratio_data[i])
            else:
                profitrate=profitrate*(1-fee_rate)
            cal=True
    return [profitrate-1,len(diff_ratio_data)]

def alpha_beta_cal(position_list,price_list):#计算alpha和beta
    diff_ratio_data = diff_ratio(price_list)
    position_list, diff_ratio_data = timeserieslength_adjust([position_list, diff_ratio_data])
    profitrate = 1
    profitrateline = []
    cal = False
    for i in range(0, len(diff_ratio_data)):
        profitrateline.append(position_list[i] * diff_ratio_data[i])
        if position_list[i] == 1:
            if cal == True:
                profitrate = profitrate * (1 + diff_ratio_data[i])

            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
        elif position_list[i] == 0:
            if cal == True:
                profitrate = profitrate * (1 - fee_rate)
            else:
                pass
        else:
            if cal == True:
                profitrate = profitrate * (1 - diff_ratio_data[i])
            else:
                profitrate = profitrate * (1 - fee_rate)
            cal = True
    return OLS(profitrateline,add_constant(diff_ratio_data)).fit().params
class indicators(object):
    def __init__(self,kline,indicator_params,judgement_params,*special_trade_function):
        if check_nulllist([kline.closepriceline,kline.openpriceline,kline.lowpriceline,kline.highpriceline,kline.timestamp])==False:
            raise AttributeError("K线数据错误")

        self.indicators_params=indicator_params
        self.judgement_params=judgement_params
        self.data=kline
        self.special_trade_function=special_trade_function #特殊的计算方式从这里导入，比如MACD，这里主要采用百度百科上的计算方式，如果有其他的计算方式，则通过这个函数导入
        self.data_after_cal=None
        self.position_list=[]
        self.save_object=standard_save
        self.interval=None
        self.symbol=None
        self.id=None

class MACD(indicators):
    def return_positionlist(self):
        self.position_list=[]
        closepriceline = self.data.closepriceline.copy()
        self.data_after_cal={
            'quick_line':[],
            'slow_line':[],
            'dif_line':[],
            'dea_line':[],
            'stick_line':[]
        }
        if self.special_trade_function==[]:
            self.position_list=self.special_trade_function[0](self.data)
        else:
            for i in range(self.indicators_params[1],len(closepriceline)):
                EMA_result_1=EMA(closepriceline[i-self.indicators_params[1]:],self.indicators_params[0])
                EMA_result_2=EMA(closepriceline[i-self.indicators_params[1]:],self.indicators_params[1])
                self.data_after_cal['quick_line'].append(EMA_result_1[0]*((self.indicators_params[0]-1))/(self.indicators_params[0]+1)\
                +closepriceline[i]*2/(self.indicators_params[0]+1))
                self.data_after_cal['slow_line'].append(EMA_result_2[0]*((self.indicators_params[1]-1))/(self.indicators_params[1]+1)\
                +closepriceline[i]*2/(self.indicators_params[1]+1))
            self.data_after_cal['dif_line']=[self.data_after_cal['quick_line'][i]-self.data_after_cal['slow_line'][i] for i in range(0,len(self.data_after_cal['slow_line']))]
            for i in range(0,len(self.data_after_cal['dif_line'])):
                if i==0:
                    self.data_after_cal['dea_line'].append(self.data_after_cal['dif_line'][0])
                else:
                    self.data_after_cal['dea_line'].append(self.data_after_cal['dif_line'][i]*0.2+0.8*self.data_after_cal['dif_line'][i-1])
            self.data_after_cal['stick_line']=[(self.data_after_cal['dif_line'][i]-self.data_after_cal['dea_line'][i])*2 for i in range(0,len(self.data_after_cal['dif_line']))]

            self.data_after_cal['dif_line'],self.data_after_cal['dea_line'],self.data_after_cal['stick_line']=timeserieslength_adjust([self.data_after_cal['dif_line'],self.data_after_cal['dea_line'],self.data_after_cal['stick_line']])
            for i in range(0,len(self.data_after_cal['dif_line'])):
                if self.judgement_params==[]:
                    if self.data_after_cal['dif_line'][i] > 0 and self.data_after_cal['dea_line'][i] > 0 and \
                            self.data_after_cal['stick_line'][i] > 0:
                        self.position_list.append(1)
                    elif self.data_after_cal['dif_line'][i] < 0 and self.data_after_cal['dea_line'][i] < 0 and \
                            self.data_after_cal['stick_line'][i] < 0:
                        self.position_list.append(-1)
                    else:
                        self.position_list.append(0)
                else:
                    judge_1=self.judgement_params[0]
                    judge_2=self.judgement_params[1]
                    if self.data_after_cal['dif_line'][i] > judge_1 and self.data_after_cal['dea_line'][i] > judge_1 and \
                            self.data_after_cal['stick_line'][i] > judge_2:
                        self.position_list.append(1)
                    elif self.data_after_cal['dif_line'][i] < judge_1 and self.data_after_cal['dea_line'][i] < judge_1 and \
                            self.data_after_cal['stick_line'][i] < judge_2:
                        self.position_list.append(-1)
                    else:
                        self.position_list.append(0)
    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list!=[]:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline)-len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly']=one_profit_rate_cal[1]*dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly']=yield_to_maxloss_yearly(self.position_list,
                                                  closepriceline[len(closepriceline)-len(self.position_list):])
            self.save_object['yield_to_stdunit']=yield_to_stdunit(self.position_list,
                                                  closepriceline[len(closepriceline)-len(self.position_list):])
            alpha_and_beta=alpha_beta_cal(self.position_list,
                                                  closepriceline[len(closepriceline)-len(self.position_list):])
            self.save_object['alpha']=alpha_and_beta[0]
            self.save_object['beta']=alpha_and_beta[1]
        else:
            raise ValueError("需要先计算仓位列表")

class KDJ(indicators):
    def return_positionlist(self):
        self.position_list=[]
        closepriceline=self.data.closepriceline.copy()
        self.data_after_cal={
            'rsv_line':max_min(closepriceline)*100,
            'K_line':[],
            'D_line':[],
            'J_line':[]
        }
        for i in range(0,len(closepriceline)):
            if i==0:
                self.data_after_cal['K_line'].append(50*2/3+self.data_after_cal['rsv_line'][0]/3)
                self.data_after_cal['D_line'].append(50 * 2 / 3 + self.data_after_cal['K_line'][0] / 3)
                self.data_after_cal['J_line'].append(3*self.data_after_cal['K_line'][0] -2*self.data_after_cal['K_line'][0])
            else:
                k=self.data_after_cal['K_line'][i-1]* 2 / 3 + self.data_after_cal['rsv_line'][i] / 3
                d=self.data_after_cal['D_line'][i - 1] * 2 / 3 + self.data_after_cal['rsv_line'][i] / 3
                self.data_after_cal['K_line'].append(k)
                self.data_after_cal['D_line'].append(d)
                self.data_after_cal['J_line'].append(3 * k - 2*d)
        for i in range(0,len(self.data_after_cal['K_line'])):
            if self.judgement_params==[]:
                if self.data_after_cal['K_line'][i]>90:
                    if self.data_after_cal['D_line'][i]>80:
                        self.position_list.append(-1)
                        continue
                    else:
                        if self.data_after_cal['J_line'][i]>90:
                            self.position_list.append(-1)
                            continue
                        else:
                            self.position_list.append(0)
                            continue
                elif self.data_after_cal['K_line'][i]<10:
                    if self.data_after_cal['D_line'][i]<20:
                        self.position_list.append(1)
                        continue
                    else:
                        if self.data_after_cal['J_line'][i]<10:
                            self.position_list.append(1)
                            continue
                        else:
                            self.position_list.append(0)
                            continue
                else:
                    self.position_list.append(0)
                    continue
            else:
                if len(self.judgement_params)<6:
                    raise ValueError("不够参数")
                if self.data_after_cal['K_line'][i]>90:
                    if self.data_after_cal['D_line'][i]>80:
                        self.position_list.append(-1)
                        continue
                    else:
                        if self.data_after_cal['J_line'][i]>90:
                            self.position_list.append(-1)
                            continue
                        else:
                            self.position_list.append(0)
                            continue
                elif self.data_after_cal['K_line'][i]<10:
                    if self.data_after_cal['D_line'][i]<20:
                        self.position_list.append(1)
                        continue
                    else:
                        if self.data_after_cal['J_line'][i]<10:
                            self.position_list.append(1)
                            continue
                        else:
                            self.position_list.append(0)
                            continue
                else:
                    self.position_list.append(0)
                    continue
    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list != []:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline) - len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly'] = one_profit_rate_cal[1] * dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly'] = yield_to_maxloss_yearly(self.position_list,
                                                                                closepriceline[
                                                                                len(closepriceline) - len(
                                                                                    self.position_list):])
            self.save_object['yield_to_stdunit'] = yield_to_stdunit(self.position_list,
                                                                    closepriceline[len(closepriceline) - len(self.position_list):])
            alpha_and_beta = alpha_beta_cal(
                self.position_list,
                closepriceline[len(closepriceline) - len(self.position_list):])
            self.save_object['alpha'] = alpha_and_beta[0]
            self.save_object['beta'] = alpha_and_beta[1]
        else:
            raise ValueError("需要先计算仓位列表")

class WR(indicators):
    def return_positionlist(self):
        self.position_list=[]
        closepriceline=self.data.closepriceline.copy()
        self.data_after_cal={
            'WR':[]
        }
        for i in range(self.indicators_params[0] if self.indicators_params[0]>0 and self.indicators_params!=[] else 0,len(closepriceline)):
            max_x = max(closepriceline[i-self.indicators_params[0]:i])
            min_x = min(closepriceline[i-self.indicators_params[0]:i])
            self.data_after_cal['WR'].append(-100*(closepriceline[i]-max_x)/(max_x-min_x))

        if self.judgement_params==[]:
            for i in range(0, len(self.data_after_cal['WR'])):
                if self.data_after_cal['WR'][i] < -80:
                    self.position_list.append(1)
                elif self.data_after_cal['WR'][i] > -20:
                    self.position_list.append(-1)
                else:
                    self.position_list.append(0)
        else:
            for i in range(0, len(self.data_after_cal['WR'])):
                if self.data_after_cal['WR'] [i]< self.judgement_params[0]:
                    self.position_list.append(1)
                elif self.data_after_cal['WR'][i] > self.judgement_params[1]:
                    self.position_list.append(-1)
                else:
                    self.position_list.append(0)

    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list != []:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline) - len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly'] = one_profit_rate_cal[1] * dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly'] = yield_to_maxloss_yearly(self.position_list,
                                                                                closepriceline[
                                                                                len(closepriceline) - len(
                                                                                    self.position_list):])
            self.save_object['yield_to_stdunit'] = yield_to_stdunit(self.position_list,
                                                                    closepriceline[
                                                                   len(closepriceline) - len(self.position_list):])
            alpha_and_beta = alpha_beta_cal(self.position_list,
                                            closepriceline[len(closepriceline) - len(self.position_list):])
            self.save_object['alpha'] = alpha_and_beta[0]
            self.save_object['beta'] = alpha_and_beta[1]
        else:
            raise ValueError("需要先计算仓位列表")

class BOLL(indicators):
    def return_positionlist(self):
        self.position_list=[]
        closepriceline = self.data.closepriceline.copy()
        self.data_after_cal={
            'BOLL_meadian':[],
            'BOLL_upper':[],
            'BOLL_downer':[]
        }
        if self.indicators_params==[] or self.indicators_params[0]<=0:
            raise AttributeError("指标参数出错")
        else:
            for i in range(self.indicators_params[0],len(closepriceline)):
                self.data_after_cal['BOLL_meadian'].append(mean(closepriceline[i-self.indicators_params[0]:i]))
                self.data_after_cal['BOLL_upper'].append(mean(closepriceline[i-self.indicators_params[0]:self.indicators_params[0]])+2*std(closepriceline[i-self.indicators_params[0]:i]))
                self.data_after_cal['BOLL_downer'].append(mean(closepriceline[i-self.indicators_params[0]:self.indicators_params[0]])-2*std(closepriceline[i-self.indicators_params[0]:i]))
            closepriceline,self.data_after_cal['BOLL_upper']=timeserieslength_adjust([closepriceline,self.data_after_cal['BOLL_upper']])
            for i in range(0,len(self.data_after_cal['BOLL_upper'])):
                if closepriceline[i]>self.data_after_cal['BOLL_upper'][i]:
                    self.position_list.append(-1)
                elif closepriceline[i]<self.data_after_cal['BOLL_downer'][i]:
                    self.position_list.append(1)
                else:
                    self.position_list.append(0)

    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list != []:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline) - len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly'] = one_profit_rate_cal[1] * dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly'] = yield_to_maxloss_yearly(self.position_list,
                                                                                closepriceline[
                                                                                len(closepriceline) - len(
                                                                                    self.position_list):])
            self.save_object['yield_to_stdunit'] = yield_to_stdunit(self.position_list,
                                                                    closepriceline[
                                                                    len(closepriceline) - len(self.position_list):])
            alpha_and_beta = alpha_beta_cal(
                self.position_list,
                closepriceline[len(closepriceline) - len(self.position_list):])
            self.save_object['alpha'] = alpha_and_beta[0]
            self.save_object['beta'] = alpha_and_beta[1]
        else:
            raise ValueError("需要先计算仓位列表")

class VR(indicators):
    def return_positionlist(self):
       self.position_list=[]
       self.data_after_cal={
       'A_line':[],
       'B_line':[],
       'VR_line':[]
       }

       check_list=[self.data.openpriceline,self.data.closepriceline,self.data.highpriceline,self.data.lowpriceline,self.data.volume]
       up_stick=[]
       if self.indicators_params[0]>0 and self.indicators_params!=[] and check_timeseries(check_list)==True:
           diff_line = diff_ratio(self.data.closepriceline)
           for i in range(self.indicators_params[0],len(self.data.closepriceline)):
                up_stick=[self.data.volume[k_num] if diff_line[k_num]>0 else 0 for k_num in range(i-int(self.indicators_params[0]),i+1)]
                down_stick = [self.data.volume[k_num] if diff_line[k_num] < 0 else 0 for k_num in range(i - int(self.indicators_params[0]), i+1)]
                same_stick=up_stick=[self.data.volume[k_num]  if diff_line[k_num]==0 else 0 for k_num in range(i-int(self.indicators_params[0]),i+1)]
                self.data_after_cal['A_line'].append(sum(up_stick)+0.5*sum(same_stick))
                self.data_after_cal['B_line'].append(sum(down_stick)+0.5*sum(same_stick))
           self.data_after_cal['VR_line']=[self.data_after_cal['A_line'][q_num]*100/self.data_after_cal['B_line'][q_num] for q_num in range(0,len(self.data_after_cal['A_line']))]
           for vr_value in range(0, len(self.data_after_cal['VR_line'])):
               if vr_value <= 70:
                   self.position_list.append(1)
               elif vr_value > 160:
                   self.position_list.append(-1)
               else:
                   self.position_list.append(0)
       elif self.indicators_params[0]<=0:
           raise IndexError("参数错误",self.indicators_params)
       elif self.indicators_params==[]:
           raise KeyError("没有指标的参数",self.indicators_params)
       else:
           raise AttributeError("K线数据有问题")
    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list != []:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline) - len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly'] = one_profit_rate_cal[1] * dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly'] = yield_to_maxloss_yearly(self.position_list,
                                                                                closepriceline[
                                                                                len(closepriceline) - len(
                                                                                    self.position_list):])
            self.save_object['yield_to_stdunit'] = yield_to_stdunit(self.position_list,
                                                                    closepriceline[
                                                                    len(closepriceline) - len(self.position_list):])
        else:
            raise ValueError("需要先计算仓位列表")

class CCI(indicators):
    def return_positionlist(self):
       self.position_list=[]
       self.data_after_cal={
       'tp_line':[],
       'ma_line':[],
       'md_line':[],
       'cci_line':[]
       }
       check_list=[self.data.openpriceline,self.data.closepriceline,self.data.highpriceline,self.data.lowpriceline,self.data.volume]
       if self.indicators_params[0]>0 and self.indicators_params!=[] and check_timeseries(check_list)==True:
           needed_ma_tp=[]
           for i in range(0,len(self.data.closepriceline)):
                self.data_after_cal['tp_line'].append((self.data.highpriceline[i]+self.data.lowpriceline[i]+self.data.closepriceline[i])/3)
           for i in range(self.indicators_params[0],len(self.data.closepriceline)):
                self.data_after_cal['ma_line'].append(mean(self.data_after_cal['tp_line'][i-self.indicators_params[0]:i+1]))
                needed_ma_tp.append(mean(self.data_after_cal['tp_line'][i-self.indicators_params[0]:i+1])-self.data_after_cal['tp_line'][i])
           abs_needed_ma_tp=[abs(each) for each in needed_ma_tp]
           for i in range(self.indicators_params[0]*2,len(self.data.closepriceline)):
                self.data_after_cal['md_line'].append(mean(abs_needed_ma_tp[i-self.indicators_params[0]:i]))
           for i in range(self.indicators_params[0]*2,len(self.data.closepriceline)):
                self.data_after_cal['cci_line'].append(0.015*(self.data_after_cal['tp_line'][i-self.indicators_params[0]*2]-self.data_after_cal['ma_line'][i-self.indicators_params[0]])/self.data_after_cal['md_line'][self.indicators_params[0]])
           for i in range(0,len(self.data_after_cal['cci_line'])):
                if self.data_after_cal['cci_line'][i]>100:
                    self.position_list.append(1)
                elif self.data_after_cal['cci_line'][i]<-100:
                    self.position_list.append(-1)
                else:
                    self.position_list.append(0)
       elif self.indicators_params[0]<=0:
           raise IndexError("参数错误",self.indicators_params)
       elif self.indicators_params==[]:
           raise KeyError("没有指标的参数",self.indicators_params)
       else:
           raise AttributeError("K线数据有问题")
    def save_profitrate(self):
        closepriceline = self.data.closepriceline.copy()
        if self.position_list != []:
            one_profit_rate_cal = profit_rate_cal(self.position_list,
                                                  closepriceline[len(closepriceline) - len(self.position_list):])

            self.save_object['profit_rate'] = one_profit_rate_cal[0]
            one_yield = yield_yearly( one_profit_rate_cal[0]  / ( dict_timelength_yearly[self.interval]* one_profit_rate_cal[1]))
            self.save_object['yearly_yield'] = one_yield
            self.save_object['cal_timelength_yearly'] = one_profit_rate_cal[1] * dict_timelength_yearly[self.interval]
            self.save_object['yield_to_maxloss_yearly'] = yield_to_maxloss_yearly(self.position_list,closepriceline[len(closepriceline) - len(self.position_list):])
            self.save_object['yield_to_stdunit'] = yield_to_stdunit(self.position_list,
                                                                    closepriceline[
                                                                    len(closepriceline) - len(self.position_list):])
            alpha_and_beta = alpha_beta_cal(
                self.position_list,
                closepriceline[len(closepriceline) - len(self.position_list):])
            self.save_object['alpha'] = alpha_and_beta[0]
            self.save_object['beta'] = alpha_and_beta[1]
        else:
            raise ValueError("需要先计算仓位列表")
        
class all_pairity_Comparision(object):#n个不同的数字货币交易对的不同周期在不同指标，不同指标参数下的全部比较,best_n函数中的judge_type参数分别可以选择按照年化收益率,夏普比率(由于获取shibor利率或者libor利率要用到外部数据，这里假设无风险利率为0，)，
    # 最大回撤，和alpha或者beta来进行排序，排序取list的开头为最大
    def __init__(self):#这里是测试和展示sample，上面test_symbol_list用的是okex下面各个数字货币与usdt的交易对，后期可以在源代码
        '''
        print('开始添加全网所有数字货币交易对列表......')

        get_allcoin_list = get_all_crptocurrency_list()
        coin_list = []
        last_coin = []
        for i in get_allcoin_list:
            if i['name'] in last_coin:
                print('这个有了')
                pass
            else:
                coin_list.append(i['symbol'])
                last_coin.append(i['name'])
        print('添加完毕,共有%d个交易对' % len(coin_list))

        '''

        global dict_interval, dict_timelength_yearly,test_symbol_list
        self.all_test=[]
        indicator_object=[
        ]
        standard_interval_symbol={
            'interval':None,
            'all_indicators':None
        }
        i_counts=0
        #for i in coin_list[:10]:
        for i in test_symbol_list[:15]:
            for j in dict_interval:
                i_counts += 1
                timetowait = abs(normalvariate(0, timetoad))
                print("稍等%s秒" % timetowait)
                sleep(timetowait)
                standard_save_object = standard_save
                standard_save_object['symbol'] = i
                standard_save_object['interval'] = j
                try:
                    one_test_kline = realtime_klineprice_aicoin_bysymbol(i, dict_interval[j])
                except:
                    print("跳过:因为", exc_info())
                    continue
                if check_nulllist([one_test_kline.closepriceline, one_test_kline.openpriceline, one_test_kline.lowpriceline,one_test_kline.highpriceline, one_test_kline.timestamp]) == False:
                    continue
                if len(one_test_kline.closepriceline) <= 100:
                    print("跳过%s %s，因为数据长度不够" % (i, j))
                    continue
                if check_constant(one_test_kline.closepriceline) == False:
                    print("全是常数，跳过")
                    continue
                if check_zero_list(one_test_kline.closepriceline)==True:
                    print("含有为0的价格，错误")
                    continue
                '''MACD计算速度太慢了，运算比较复杂，而且一般收益都比其他差，不用它了
                for p in range(5, 11):
                    for k in range(12,24):
                        a=MACD(one_test_kline, [p,  k], [])
                        a.interval=j
                        a.symbol=i
                        a.id='MACD'
                        indicator_object.append(a)
                        #print("增加参数为 %d和%d 在 %s  和  %s 的MACD系统" % (p, k, i, j))
                '''

                for p in range(5, 30):
                    a = BOLL(one_test_kline, [p], [])
                    a.interval = j
                    a.symbol = i
                    a.id = 'BOLL'

                    indicator_object.append(a)
                    # print("增加参数为 %d 在 %s  和  %s 的BOLL系统" % (p, i, j))

                for p in range(5, 30):
                    a = VR(one_test_kline, [p], [])
                    a.interval = j
                    a.symbol = i
                    a.id = 'VR'

                    indicator_object.append(a)
                for p in range(5, 30):
                    a = CCI(one_test_kline, [p], [])
                    a.interval = j
                    a.symbol = i
                    a.id = 'CCI'

                    indicator_object.append(a)
                for p in range(1, 20):
                    for k in range(6, 22):
                        a = KDJ(one_test_kline, [p, p + k], [])
                        a.interval = j
                        a.symbol = i
                        a.id = 'KDJ'

                        # print("增加参数为 %d和%d 在 %s  和  %s 的KDJ系统" % (p, k, i, j))
                        indicator_object.append(a)

                for p in range(3, 21):
                    a = WR(one_test_kline, [p], [])
                    a.interval = j
                    a.symbol = i
                    a.id = 'WR'

                    # print("增加参数为 %d 在 %s  和  %s 的WR系统" % (p, i, j))
                    indicator_object.append(a)

                for n in indicator_object:
                    print("---------------------------------------------------------------")
                    n.return_positionlist()
                    print("%s|%s|%s" % (n.interval, n.symbol, n.id))
                    n.save_profitrate()
                    n.save_object = n.save_object.copy()
                    print(n.save_object, "|指标参数", n.indicators_params)
                    n.data = None
                    n.data_after_cal = None

                one_new_save_object = standard_interval_symbol.copy()
                one_new_save_object['interval'] = j
                one_new_save_object['symbol'] = i
                one_new_save_object['all_indicators'] = indicator_object.copy()
                self.all_test.append(one_new_save_object)
                indicator_object = []
                print("完成进度%f persents" % (i_counts * 100 / (len(dict_interval) * len(test_symbol_list[:15 ]))))
    def best_n(self,n=None,judge_type='yield_to_stdunit'):
        print("共有%d个数据需要排序" % (len(self.all_test) * len(self.all_test[0]['all_indicators'])))
        if n <= len(self.all_test) * len(self.all_test[0]['all_indicators']):
            return sorted_list_all(self.all_test,n, judge_type=judge_type)
        elif n == None:
            return sorted_list_all(self.all_test, judge_type=judge_type)
        else:
            raise ValueError("请求参数值错误")

class single_pairity_Comparision(object):#给定数字货币交易对的不同周期在不同指标，不同指标参数下的全部比较,best_n函数中的judge_type参数分别可以选择按照年化收益率,夏普比率(由于获取shibor利率或者libor利率要用到外部数据，这里假设无风险利率为0，)，
    # 最大回撤，和alpha或者beta来进行排序，排序取list的开头为最大
    def __init__(self,my_symbol):#my_symbol是aicoin的symbol字段，例如etcusdt:huobipro
        global dict_symbol, dict_interval, dict_timelength_yearly
        self.all_test=[]
        indicator_object=[
        ]
        standard_interval_symbol={
            'interval':None,
            'symbol':None,
            'all_indicators':None
        }
        i_counts=0
        i=my_symbol
        for j in dict_interval:
            i_counts += 1
            timetowait = abs(normalvariate(0, timetoad))
            print("稍等%s秒" % timetowait)
            sleep(timetowait)
            standard_save_object = standard_save
            standard_save_object['symbol'] = i
            standard_save_object['interval'] = j
            try:
                one_test_kline = realtime_klineprice_aicoin_bysymbol(i, dict_interval[j])
            except:
                print("跳过:因为", exc_info())
                continue
            if check_nulllist([one_test_kline.closepriceline, one_test_kline.openpriceline, one_test_kline.lowpriceline,one_test_kline.highpriceline, one_test_kline.timestamp]) == False:
                continue
            if len(one_test_kline.closepriceline) <= 50:
                print("跳过%s %s，因为数据长度不够" % (i, j))
                continue
            if check_constant(one_test_kline.closepriceline) == False:
                print("全是常数，跳过")
                continue
            '''MACD计算速度太慢了，运算比较复杂，而且一般收益都比其他差，不用它了
            for p in range(5, 11):
                for k in range(12,24):
                    a=MACD(one_test_kline, [p,  k], [])
                    a.interval=j
                    a.symbol=i
                    a.id='MACD'
                    indicator_object.append(a)
                    #print("增加参数为 %d和%d 在 %s  和  %s 的MACD系统" % (p, k, i, j))
            '''

            for p in range(5, 30):
                a = BOLL(one_test_kline, [p], [])
                a.interval = j
                a.symbol = i
                a.id = 'BOLL'

                indicator_object.append(a)
                # print("增加参数为 %d 在 %s  和  %s 的BOLL系统" % (p, i, j))

            for p in range(5, 30):
                a = VR(one_test_kline, [p], [])
                a.interval = j
                a.symbol = i
                a.id = 'VR'

                indicator_object.append(a)
            for p in range(5, 30):
                a = CCI(one_test_kline, [p], [])
                a.interval = j
                a.symbol = i
                a.id = 'CCI'

                indicator_object.append(a)
            for p in range(1, 20):
                for k in range(6, 22):
                    a = KDJ(one_test_kline, [p, p + k], [])
                    a.interval = j
                    a.symbol = i
                    a.id = 'KDJ'

                    # print("增加参数为 %d和%d 在 %s  和  %s 的KDJ系统" % (p, k, i, j))
                    indicator_object.append(a)

            for p in range(3, 21):
                a = WR(one_test_kline, [p], [])
                a.interval = j
                a.symbol = i
                a.id = 'WR'

                # print("增加参数为 %d 在 %s  和  %s 的WR系统" % (p, i, j))
                indicator_object.append(a)

            for n in indicator_object:
                print("---------------------------------------------------------------")
                n.return_positionlist()
                print("%s|%s|%s" % (n.interval, n.symbol, n.id))
                n.save_profitrate()
                n.save_object=n.save_object.copy()
                print(n.save_object, "|指标参数", n.indicators_params)
                n.data=None
                n.data_after_cal=None

            one_new_save_object = standard_interval_symbol.copy()
            one_new_save_object['interval'] = j
            one_new_save_object['symbol'] = i
            one_new_save_object['all_indicators'] = indicator_object.copy()
            self.all_test.append(one_new_save_object)
            indicator_object = []
    def best_n(self,n=None,judge_type='yield_to_stdunit'):
        print("共有%d个数据需要排序"%(len(self.all_test)*len(self.all_test[0]['all_indicators'])))
        if n <=len(self.all_test)*len(self.all_test[0]['all_indicators']):
            return sorted_list_all(self.all_test,n,judge_type=judge_type)
        elif n==None:
            return sorted_list_all(self.all_test, judge_type=judge_type)
        else:
            raise ValueError("请求参数值错误")
def sorted_list_all(all_comparision,n=None,judge_type='yield_to_stdunit'):
    all=[]

    for i in all_comparision:
        for j in i['all_indicators']:
            str_params=''
            for each_param in j.indicators_params:
                str_params=str_params+'/'+str(each_param)
            all.append([j.save_object[judge_type],j.symbol+"/"+j.interval+"/"+j.id+str_params])
    if n==None:
        n=len(all)
    else:
        pass
    test_line = [k[0] for k in all]
    while check_max_list(test_line) == False:
        counts=True
        for each_in_total_maxlist in range(0, len(all) - 1):
            last_index =all[each_in_total_maxlist-1]
            next_index=all[each_in_total_maxlist+1]
            if all[each_in_total_maxlist][0] >= all[each_in_total_maxlist + 1][0]:
                pass
            else:
                if counts==True and next_index> all[each_in_total_maxlist]>last_index and each_in_total_maxlist!=0:
                    print("计算位置移动到%f persents的位置"%(each_in_total_maxlist*100/(len(all)-1)))
                    counts=False
                all[each_in_total_maxlist], all[each_in_total_maxlist + 1] = all[each_in_total_maxlist + 1], all[each_in_total_maxlist]
        test_line = [k[0] for k in all]
    return all[:n]


start_time=time()
A=all_pairity_Comparision()
B1=A.best_n(n=500)
B2=A.best_n(n=500,judge_type='yield_to_maxloss_yearly')
B3=A.best_n(n=500,judge_type='yearly_yield')
B4=A.best_n(n=500,judge_type='alpha')

end_time=time()
print("一共用了%f秒"%(end_time-start_time))
'''
a=single_pairity_Comparision('etcusdt:huobipro')

b1=a.best_n(n=500)
b2=a.best_n(n=500,judge_type='yield_to_maxloss_yearly')
b3=a.best_n(n=500,judge_type='yearly_yield')
b4=a.best_n(n=500,judge_type='alpha')
'''
print("dsfsdfsdf")
print("sdgsdgdfgfdg")



