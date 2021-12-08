# coding=UTF-8
'''
主要做的市场：BTC-okex永续合约
#开平仓信号
主干指标:宏观指数指标做买卖点
过滤指标:近期5分钟价格的上涨幅度(价格变化率绝对值)，如果近期5分钟单个分钟价格变化率绝对值大于3%，如果与现在仓位同方向，不管，如果相反方向，果断平仓，对突发波动更为敏感

#仓位设置
仓位大小的选择，在初代版本先设置为每次开一单位合约

#止损止盈系统
单笔亏损超过3%,或者单笔盈利超过3%就关停订单

#获取实时行情
最新价格

#计算各种参考数值指标系统
判断宏观市场状况：数字货币主流币市场指数

#交易系统状态展示系统:实时收益率，最大回撤等指标计算

#日志交易功能:开始订单，结束订单，每隔5分钟更新账户实际盈利状态/市场实际的

# 获取某个合约的用户配置 （5次/2s）
        # result = swapAPI.get_settings('')
        # 设定某个合约的杠杆 （5次/2s）
        # result = swapAPI.set_leverage('', '', '')
        # 账单流水查询 （5次/2s）
        # result = swapAPI.get_ledger('')
        # 下单 （40次/2s）
        # result = swapAPI.take_order('', '', '', '', order_type='0', client_oid='', match_price='0')
        # 批量下单 （20次/2s）
        # result = swapAPI.take_orders('', [
        #         {'client_oid': '', 'type': '', 'price': '', 'size': ''},
        #         {'client_oid': '', 'type': '', 'price': '', 'size': ''}
        #     ])
        # 撤单 （40次/2s）
        # result = swapAPI.revoke_order('', '')
        # 批量撤单 （20次/2s）
        # result = swapAPI.revoke_orders('', ids=['', ''])
        # 获取所有订单列表 （20次/2s）
        # result = swapAPI.get_order_list('', '')
        # 获取订单信息 （10次/2s）
        # result = swapAPI.get_order_info('', '')
        # 获取成交明细 （10次/2s）
        # result = swapAPI.get_fills('')
        # 获取合约挂单冻结数量 （5次/2s）
        # result = swapAPI.get_holds_amount('')
        # 委托策略下单 （40次/2s）
        # result = swapAPI.take_order_algo('', '', '', '', trigger_price='', algo_price='', algo_type='')
        # 委托策略撤单 （20 次/2s）
        # result = swapAPI.cancel_algos('', [''], '')
        # 获取委托单列表 （20次/2s）
        # result = swapAPI.get_order_algos('', '', algo_id='', status='')
        # 获取账户手续费费率 （5次/2s）
        # result = swapAPI.get_trade_fee()
        # 市价全平（2次/2s）
        # result = swapAPI.close_position('', '')
        # 撤销所有平仓挂单（5次/2s）
        # result = swapAPI.cancel_all('', '')
        # 公共-获取合约信息 （20次/2s）
        # result = swapAPI.get_instruments()
        # 公共-获取深度数据 （20次/2s）
        # result = swapAPI.get_depth('', '', '')
        # 公共-获取全部ticker信息 （20次/2s）
        # result = swapAPI.get_ticker()
        # 公共-获取某个ticker信息 （20次/2s）
        self.last_price= float(self.swapAPI.get_specific_ticker('BTC-USD-SWAP')['last'])
        # 公共-获取成交数据 （20次/2s）
        #result = self.swapAPI.get_trades('BTC-USD-SWAP')
        #公共-获取K线数据 （20次/2s）
        #self.last_price = swapAPI.get_kline('BTC-USD-SWAP', '')
        # 公共-获取指数信息 （20次/2s）
        # result = swapAPI.get_index('')
        # 公共-获取法币汇率 （20次/2s）
        # result = swapAPI.get_rate()
        # 公共-获取平台总持仓量 （20次/2s）
        # result = swapAPI.get_holds('')
        # 公共-获取当前限价 （20次/2s）
        # result = swapAPI.get_limit('')
        # 公共-获取强平单 （20次/2s）
        # result = swapAPI.get_liquidation('', '')
        # 公共-获取合约资金费率 （20次/2s）
        # result = swapAPI.get_funding_time('')
        # 公共-获取合约标记价格 （20次/2s）
        # result = swapAPI.get_mark_price('')
        # 公共-获取合约历史资金费率 （20次/2s）
        # result = swapAPI.get_historical_funding_rate('')
'''
import sys
import urllib3
import json
import datetime
from time import time,sleep
from requests import get
import requests
from sys import exc_info
from csv import writer,reader
from MarcoIndex import Get_index_kline
index_top=None

defined_size=[str(1),str(13)]##合约按张为单位
define_fee_rate=0.0005



def get_ticker():
    url='https://www.okex.me/v2/perpetual/pc/public/contracts/BTC-USD-SWAP/ticker?t='+str(int(time()))
    get_result=get(url)
    if get_result.status_code==200:
        return float(json.loads(get_result.text)['data']['close'])
    else:
        print("没有价格")
#获取内部的指标数据
def get_marco_index():
    results=Get_index_kline('30m','BTC',not_yield=False)
    newest_some=results[0].closepriceline[len(results[0].closepriceline)-64:len(results[0].closepriceline)]
    lasting_time={
        'side':0,
        'time':0
    }
    three_list=[0,0,0]
    for i in range(0,len(newest_some)):
        if abs(newest_some[i])<0.5:
            three_list[0]+=(1/64)
        elif abs(newest_some[i])>=0.5 and newest_some[i]>=0.5:
            three_list[1]+=(1/64)
        else:
            three_list[2]+=(1/64)
    return [three_list,results[3].f_pvalue,newest_some]
class trader(object):
    def __init__(self):
        self.api_key='cec0d9cd-6400-49da-a54f-af6a1261f814'
        self.secret_key='70CED80A44FD34D2F2C535BE1BB301B2'
        self.passphrase='14567ty'
        get_indexandcorr=get_marco_index()
        self.now_marco_indicator_level =get_indexandcorr [0]
        self.corr_to_marco =get_indexandcorr[1]
        # 所有合约持仓信息 （1次/10s）
        #self.contract_holding_all=self. swapAPI.get_position()
        # 单个合约持仓信息 （20次/2s）
        self.marco_indicator_level_newest = get_indexandcorr[2][len(get_indexandcorr[2]) - 1]
        self.active_order_side = 0
        self.active_order_avg_cost = 0
        self.active_order_position = 0
        self.origin_rate=1
        self.change_kind=[]
        '''

        csvreader=reader(open("trader_log_yield.csv", 'r',encoding='utf-8'))
        record_list = []
        for i in csvreader:
            record_list.append(i)
        self.active_order_side=int(record_list[len(record_list)-1][1])
        self.active_order_position=int(record_list[len(record_list)-1][2])
        self.active_order_avg_cost=float(record_list[len(record_list)-1][3])   
        self.origin_rate= float(record_list[len(record_list)-1][10])  
        print("读取数据完毕,现在继承的仓位为:%d,收益率为%f"%(self.active_order_side,self.origin_rate))
        '''
        self.name='LAIXINGLIN-MARCO-TRADER'
        print("finished")
    def detecter(self):#每隔2秒查看是否有突然的价格涨跌，然后止盈或者止损
        log_information=[]
        global defined_size,define_fee_rate
        self.last_price = get_ticker()
        now_rate=(self.last_price-self.active_order_avg_cost)*self.active_order_side/self.active_order_avg_cost if self.active_order_avg_cost!=0 else 0
        if self.active_order_position!=0:
            if now_rate>=0.02 or abs(self.marco_indicator_level_newest)<=1:
                self.origin_rate = self.origin_rate + now_rate - define_fee_rate
                self.active_order_side = 0
                self.active_order_avg_cost = 0
                self.active_order_position = 0
            elif now_rate<=-0.015:
                self.origin_rate = self.origin_rate + now_rate - define_fee_rate
                self.active_order_side = 0
                self.active_order_avg_cost = 0
                self.active_order_position = 0
            else:#没有超过止盈止损线，就不用管了
                print("当前的收益率:%s，当前仓位方向:%d，当前价格%s,当前指标水平:"%(now_rate,self.active_order_side,self.last_price))
                print(self.now_marco_indicator_level,self.marco_indicator_level_newest)
                pass
        else:#没有开仓，略过
            print("交易休息中,现价:%f,现在的corr:%f,已经实现的收益率:%f"%(self.last_price,self.corr_to_marco,self.origin_rate))
            print("现在的指数：",self.now_marco_indicator_level,self.marco_indicator_level_newest)
        '''
        日志记录代码
        '''
        if log_information==[]:
            pass
        else:
            self.log(log_information)
        '''
                统一的修改现在状态的代码
                '''
    def update_myself(self):#
        global defined_size,define_fee_rate
        self.last_price=get_ticker()
        log_information=[]
        get_indexandcorr = get_marco_index()
        self.change_kind.append(self.now_marco_indicator_level) 
        if len(self.change_kind)>=100:
            del self.change_kind[0]
        else:
            pass
        self.now_marco_indicator_level = get_indexandcorr[0]
        self.marco_indicator_level_newest=get_indexandcorr[2][len(get_indexandcorr[2])-1]
        self.corr_to_marco = get_indexandcorr[1]
        self.record_data()
        
        #下单判断。满足开平仓条件，如果已经开仓，则判断现有是否现有仓位，如果是已经开仓了而且是与现在判断的方向一致的则pass，如果不是，就平了原来的仓位然后
        gap=[self.change_kind[len(self.change_kind)-1][0]-self.change_kind[len(self.change_kind)-1-12][0] ,self.change_kind[len(self.change_kind)-1][1]-self.change_kind[len(self.change_kind)-1-12][1] ,self.change_kind[len(self.change_kind)-1][2]-self.change_kind[len(self.change_kind)-1-12][2]] if len(self.change_kind)>12 else [0,0,0]
        print("各状态转换差值",gap)
        if self.corr_to_marco<=0.1 and self.marco_indicator_level_newest>=3 :
            if self.active_order_position==0:
                self.origin_rate=self.origin_rate-define_fee_rate
                self.active_order_side=-1
                self.active_order_avg_cost=self.last_price
                self.active_order_position=-1
                log_information.append("判断开空")
            elif self.active_order_position!=0 and self.active_order_side==-1:
                self.origin_rate = self.origin_rate - define_fee_rate*2
                self.active_order_side = -1
                self.active_order_avg_cost = self.last_price
                self.active_order_position = -1
                log_information.append("与原来相反，判断多转到空")
            else:
                pass

        elif self.corr_to_marco<=0.1 and self.marco_indicator_level_newest<=-3:
            if self.active_order_position==0:
                self.origin_rate=self.origin_rate-define_fee_rate
                self.active_order_side=1
                self.active_order_avg_cost=self.last_price
                self.active_order_position=1
                log_information.append("判断开多")
            elif self.active_order_position!=0 and self.active_order_side==-1:
                self.origin_rate = self.origin_rate - define_fee_rate*2
                self.active_order_side = 1
                self.active_order_avg_cost = self.last_price
                self.active_order_position =1
                log_information.append("与原来相反，判断空转到多")
            else:
               pass
        else:
            if self.active_order_position!=0:
                self.active_order_avg_cost=0
                self.active_order_position=0
                self.active_order_side=0
                self.origin_rate=self.origin_rate-define_fee_rate
            else:
                print("正常开仓中")
            if self.corr_to_marco>=0.1:
                log_information.append("相关性变弱")
                print("相关性变弱")
            else:
                pass
            print("更新完毕，但不满足开仓条件，现价:%f，现在的corr-gap:%f"%(self.last_price,self.corr_to_marco))
            print("现在的指标", self.now_marco_indicator_level)    
        #止盈止损判断
        
        
        ##日志记录代码
        
        self.record_data()
        self.log(log_information)

    def record_data(self):
        save_data=[
            time(),
            self.last_price,
            self.now_marco_indicator_level[0],
            self.now_marco_indicator_level[1],
            self.now_marco_indicator_level[2],
            self.marco_indicator_level_newest,
            self.corr_to_marco,
            self.origin_rate
        ]
        with open('record_new_yield_year.csv','a',newline='',encoding='UTF8') as log_writer:
            csv_log=writer(log_writer)
            csv_log.writerow(save_data)
    def log(self,information_to_log):
        save_data=[
            time(),
            self.active_order_side if self.active_order_side!=None else 0,
            self.active_order_position if self.active_order_position!=None else 0,
            self.active_order_avg_cost if self.active_order_avg_cost!=None else 0,
            self.last_price,
            self.now_marco_indicator_level[0],
            self.now_marco_indicator_level[1],
            self.now_marco_indicator_level[2],
            self.marco_indicator_level_newest,
            self.corr_to_marco,
            self.origin_rate
        ]
        if information_to_log!=[]:
            for i in information_to_log:
                save_data.append(i)
        else:
            pass
        with open('trader_log_yield_year.csv','a',newline='',encoding='UTF8') as log_writer:
            csv_log=writer(log_writer)
            csv_log.writerow(save_data)
def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"
last_update_time=time()
def main_loop():
    last_update_time=time()
    mytrader=trader()
    while True:
        print("------------------1dmin--------------------------")
        
        if time()-last_update_time>=1800:
            mytrader.update_myself()
            last_update_time=time()
        else:
            print("离下次更新还有%f秒"%(1800-(time()-last_update_time)))
            pass
        mytrader.detecter()
        sleep(3)
while True:
    sleep(2.5)
    try:
        main_loop()
    except (ConnectionRefusedError,urllib3.exceptions.NewConnectionError,requests.exceptions.ConnectionError,KeyError):
        main_loop()
