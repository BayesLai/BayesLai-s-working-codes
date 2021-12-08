from numpy import mean,std,array
BOLL_paraqms=100
from random import normalvariate
from statsmodels.api import OLS,add_constant
from time import time,sleep
from requests import get
from sys import exc_info
from json import loads
from csv import writer
from DataProcess import normalize
class kline(object):
    def __init__(self):
        self.closepriceline=[]
        self.openpriceline=[]
        self.highpriceline=[]
        self.lowpriceline=[]
        self.timeline=[]
        self.volumeline=[]
def get_last_prices(interval='900',size='1000'):
    url="https://www.okex.me/v2/perpetual/pc/public/instruments/BTC-USD-SWAP/candles?granularity="+interval+"&size="+size+"&t="+str(int(time()))
    get_result=get(url)
    kline_toreturn=kline()
    if get_result.status_code==200:
        try:
            json_data=loads(get_result.text)
        except:
            print(get_result.text)
            raise ValueError("valueerror",exc_info())
        for i in range(0,len(json_data['data'])):
            kline_toreturn.closepriceline.append(float(json_data['data'][i][4]))
            kline_toreturn.openpriceline.append(float(json_data['data'][i][1]))
            kline_toreturn.highpriceline.append(float(json_data['data'][i][3]))
            kline_toreturn.lowpriceline.append(float(json_data['data'][i][2]))
            kline_toreturn.timeline.append(json_data['data'][i][0])
            kline_toreturn.volumeline.append(float(json_data['data'][i][5]))
        return kline_toreturn
    else:
        print(exc_info())
        return None
def BOLL(data,params):
    global  BOLL_paraqms
    params=abs(params)
    BOLL_median=[mean(data[i-BOLL_paraqms:i]) for i in range(BOLL_paraqms,len(data))]
    BOLL_up=[mean(data[i-BOLL_paraqms:i])+std(data[i-BOLL_paraqms:i])*params for i in range(BOLL_paraqms,len(data))]
    BOLL_down=[mean(data[i-BOLL_paraqms:i])-std(data[i-BOLL_paraqms:i])*params for i in range(BOLL_paraqms,len(data))]
    BOLL_std=[std(data[i-BOLL_paraqms:i])*params for i in range(BOLL_paraqms,len(data))]
    return [BOLL_up,BOLL_median,BOLL_down,BOLL_std]
def high_and_low_s(data,space_nums=2):
    rate_estimated=1000/(data[len(data)-1]*space_nums)
    nums_maxmin=0
    nums_order=2
    copy_data=data.copy()
    maxmin_list=[]
    while (max(copy_data)-min(copy_data))/(max(copy_data)+min(copy_data)/2)>=rate_estimated:
        nums_maxmin+=1
        maxmin_list.append([data.index(max(copy_data)),max(copy_data),data.index(min(copy_data)),min(copy_data)])
        del copy_data[copy_data.index(max(copy_data))]
        del copy_data[copy_data.index(min(copy_data))]
    aonther_data=data.copy()
    i=0
    if maxmin_list==[]:
        return None
    else:
        now_index_inmaxminlist = maxmin_list[0][0]
        max_index_list = [i[0] for i in maxmin_list]
        min_index_list = [i[2] for i in maxmin_list]
        for i in range(0, int(len(maxmin_list) / 2) + 1):
            if now_index_inmaxminlist + i in max_index_list or now_index_inmaxminlist - i in max_index_list:
                pass
            else:
                nums_order += 1
        now_index_inmaxminlist = maxmin_list[0][2]
        for i in range(0, int(len(maxmin_list) / 2) + 1):
            if now_index_inmaxminlist + i in min_index_list or now_index_inmaxminlist - i in min_index_list:
                pass
            else:
                nums_order += 1
        return [nums_order, maxmin_list]
def smooth_by_order(data):
    gets_data=high_and_low_s(data,space_nums=3)
    order_lists=[[1 for i in range(0,len(data))]]
    for index_r in range(1,gets_data[0]+1):
        order_lists.append([i**index_r  for i in range(0,len(data))])
    order_lists=order_lists if len(order_lists)<=5 else order_lists[:5]
    return OLS(data,array(order_lists[:5]).T).fit()
class Advanced_Grid(object):
    def __init__(self):
        self.kline=get_last_prices()
        self.BOLL=BOLL(self.kline.closepriceline,1.96)
        ok_min = high_and_low_s(self.kline.closepriceline)
        self.max_min_list = ok_min[1]
        print("最近的非线性阶数:", ok_min[0])
        self.last_price=self.kline.closepriceline[len(self.kline.closepriceline)-1]
        self.std_line=self.BOLL[3]
        self.upper_sky=self.max_min_list[0][1]
        self.upper_cloud=self.BOLL[0][len(self.BOLL[0])-1]
        self.shoe=self.BOLL[1][len(self.BOLL[1])-1]
        self.head=self.kline.closepriceline[len(self.kline.closepriceline)-1]
        self.downer_mud=self.BOLL[2][len(self.BOLL[2])-1]
        self.downer_land=self.max_min_list[0][3]
        self.last_status=[None,None,None,None,None]
        self.location_global=(self.head-self.downer_land)/(self.upper_sky-self.downer_land)
        self.location_inBOLL=(self.head-self.downer_mud)/(self.upper_cloud-self.downer_mud)

        self.BOLL_level=(self.shoe-self.downer_land)/(self.upper_sky-self.downer_land)

        self.gap=self.std_line[len(self.std_line)-1]

        self.status=[None,None,None,None,None]
        self.maxmin_status = [None, None, None]
        # 模拟仓位
        self.buysell = 0
        self.costprice = 0
        self.feerate = 0.0005
        self.profitrate = 1
        self.realtime_profitrate = 1
        self.BOLL_lastingtime_for_deal = 0

        self.cal_my_status()
        self.judge_mystatus(20)

    def cal_my_status(self):
        print("--------开始计算当前状态----------")
        print("Time:",time())
        self.status=self.last_status
        if self.location_global>0.7:

            self.status[0]=1
        elif self.location_global<0.3:
            self.status[0]=-1
        else:
            self.status[0]=0
        if self.location_inBOLL>0.6:
            self.status[1]=1
        elif self.location_inBOLL<0.4:
            self.status[1]=-1
        else:
            self.status[1]=0

        if self.status[0]==1:
            max_index_list = [self.max_min_list[i][0] for i in range(0, len(self.max_min_list))]
            max_price_index_list = [self.max_min_list[i][1] for i in range(0, len(self.max_min_list))]
            estimated_result = OLS(max_price_index_list, add_constant(max_index_list)).fit()
            if estimated_result.params[1] > 0 and estimated_result.pvalues[1] < 0.05:
                self.status[2]= 1
            elif estimated_result.params[1] < 0 and estimated_result.pvalues[1] < 0.05:
                self.status[2]= -1
            else:
                self.status[2]=0
        elif self.status[0]==-1:
            max_index_list = [self.max_min_list[i][3] for i in range(0, len(self.max_min_list))]
            max_price_index_list = [self.max_min_list[i][2] for i in range(0, len(self.max_min_list))]
            estimated_result = OLS(max_price_index_list, add_constant(max_index_list)).fit()
            if estimated_result.params[1] < 0 and estimated_result.pvalues[1] <0.05:
                self.status[2] = -1
            elif estimated_result.params[1] > 0 and estimated_result.pvalues[1] > 0.05:
                self.status[2]= 1
            else:
                self.status[2]=0
        else:
            max_index_list = [self.max_min_list[i][3] for i in range(0, len(self.max_min_list))]
            max_price_index_list = [self.max_min_list[i][2] for i in range(0, len(self.max_min_list))]
            estimated_result = OLS(max_price_index_list, add_constant(max_index_list)).fit()
            if estimated_result.params[1] < 0 and estimated_result.pvalues[1] < 0.02:
                self.status[2] = -1
            elif estimated_result.params[1] > 0 and estimated_result.pvalues[1] > 0.02:
                self.status[2] = 1
            else:
                self.status[2] = 0
            self.status[2]=0

        if self.gap<=120:
            self.status[3] = 2
        elif 120<self.gap<=180:
            self.status[3]=1
        else:
            self.status[3] = 0

        reverse_trendtest_line=self.kline.closepriceline[len(self.kline.closepriceline)-1-96*3:]
        xline=[i for i in range(0,len(reverse_trendtest_line))]
        x_2_line=[i**2 for i in range(0,len(reverse_trendtest_line))]
        reverse_ols=OLS(reverse_trendtest_line,add_constant(array([xline,x_2_line]).T)).fit()
        if reverse_ols.params[2]<0 and reverse_ols.pvalues[2]<0.05:
            self.status[4]=-1
        elif reverse_ols.params[2]>0 and reverse_ols.pvalues[2]<0.05:
            self.status[4]=1
        else:
            self.status[4]=0
        self.trend_location=[estimated_result.params[1],estimated_result.pvalues[1]]
        self.Possible_Reverse=[reverse_ols.params[2],reverse_ols.pvalues[2]]
        print("Price",self.last_price)
        print("global location:", self.location_global)
        print("BOLL location:",self.location_inBOLL)
        print("trend location:",[estimated_result.params[1],estimated_result.pvalues[1]] if self.status[2]!=0 else "None trend")
        print("Variance:",self.gap)
        print("Possible Reverse:",[reverse_ols.params[2],reverse_ols.pvalues[2]],'-->None' if self.status[4]==0 else '-->It did')
    def log(self,information):
        with open("Advanced Grid.csv",'a',newline='')as myfile:
            csvwriter=writer(myfile)
            senddata=[time()]
            senddata.append(self.last_price)
            for i in self.status:
                senddata.append(i)
            for i in self.maxmin_status:
                senddata.append(i)
            senddata.append(self.location_global)
            senddata.append(self.location_inBOLL)
            senddata.append(self.trend_location[0])
            senddata.append(self.trend_location[1])
            senddata.append(self.gap)
            senddata.append(self.Possible_Reverse[0])
            senddata.append(self.Possible_Reverse[1])
            senddata.append(self.buysell)
            senddata.append(self.costprice)
            senddata.append(self.profitrate)
            senddata.append(self.realtime_profitrate)
            senddata.append(information)

            csvwriter.writerow(senddata)
    def judge_mystatus(self,total_unit):
        list_buy=[
            [1, 1, 1, 1, 1],#全局高位，BOLL高位，高低波段明显正向，波动率较低，反转趋势上转
            [-1, 1, -1, 1, 1],#全局低位，BOLL高位，高低波段明显反向，波动率较低，反转趋势上转
            [1, 1, 1, 1, 0],#全局高位，BOLL高位，高低波段正向明显，波动率较低，反转趋势不明显
            [1, -1, -1, 1, 0],#全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势不明显
            [-1, 1, 1, 1, 1],#全局低位，BOLL高位，高低波段正向明显，波动率较低，反转趋势明显
            [1, 1, 1, 2, 1],  # 全局高位，BOLL高位，高低波段明显正向，波动率低，反转趋势上转
            [-1, 1, -1, 2, 1],  # 全局低位，BOLL高位，高低波段明显反向，波动率低，反转趋势上转
            [1, 1, 1, 2, 0],  # 全局高位，BOLL高位，高低波段正向明显，波动率低，反转趋势不明显
            [1, -1, -1, 2, 0],  # 全局高位，BOLL低位，高低波段负向明显，波动率低，反转趋势不明显
            [-1, 1, 1, 2, 1],  # 全局低位，BOLL高位，高低波段正向明显，波动率低，反转趋势明显
            [-1, -1, 1, 2, 1],#全局低位，BOLL低位，高低波段正向明显，波动率低，反转趋势明显
            [1, 1, -1, 2, 0]#全局高位，BOLL高位，高低波段正向明显，波动率低，反转趋势不明显
        ]
        list_sell=[
            [-1, -1, -1, 1, -1],#全局低位，BOLL低位，高低波段负向明显，波动率较低，反转趋势下转
            [1, -1, -1, 1, -1],  # 全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势下转
            [-1, 1, -1, 1, 0],#全局低位，BOLL高位，高低波段负向明显，波动率较低，反转趋势不明显
            [1, -1, 0, 1, -1],#全局高位，BOLL低位，高低波段不明显，波动率较低，反转趋势负向
            [1, -1, -1, 1, -1],# 全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势明显
            [-1, -1, -1, 2, -1],  # 全局低位，BOLL低位，高低波段负向明显，波动率低，反转趋势下转
            [1, -1, -1, 2, -1],  # 全局高位，BOLL低位，高低波段负向明显，波动率低，反转趋势下转
            [-1, 1, -1, 2, 0],  # 全局低位，BOLL高位，高低波段负向明显，波动率低，反转趋势不明显
            [1, -1, 0, 2, -1],  # 全局高位，BOLL低位，高低波段不明显，波动率低，反转趋势负向
            [1, -1, -1, 2, -1],  # 全局高位，BOLL低位，高低波段负向明显，波动率低，反转趋势明显
            #[0, -1, 1, 0, -1]#全局中，BOLL低位，高低波段负向明显，波动率低，反转趋势下转
        ]
        dict_buy=[
            '全局高位，BOLL高位，高低波段明显正向，波动率较低，反转趋势上转',
            '全局低位，BOLL高位，高低波段明显反向，波动率较低，反转趋势上转',
            '全局高位，BOLL高位，高低波段正向明显，波动率较低，反转趋势不明显',
            '全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势不明显',
             '全局低位，BOLL高位，高低波段正向明显，波动率较低，反转趋势明显',
            '全局高位，BOLL高位，高低波段明显正向，波动率低，反转趋势上转',
            '全局低位，BOLL高位，高低波段明显反向，波动率低，反转趋势上转',
            '全局高位，BOLL高位，高低波段正向明显，波动率低，反转趋势不明显',
            '全局高位，BOLL低位，高低波段负向明显，波动率低，反转趋势不明显',
            '全局低位，BOLL高位，高低波段正向明显，波动率低，反转趋势明显',
        '全局低位，BOLL低位，高低波段正向明显，波动率低，反转趋势明显',
            '全局高位，BOLL高位，高低波段正向明显，波动率低，反转趋势不明显'
        ]
        dict_sell=[
            '全局低位，BOLL低位，高低波段负向明显，波动率较低，反转趋势下转',
            '全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势下转',
            '全局低位，BOLL高位，高低波段负向明显，波动率较低，反转趋势不明显',
            '全局高位，BOLL低位，高低波段不明显，波动率较低，反转趋势负向',
            '全局高位，BOLL低位，高低波段负向明显，波动率较低，反转趋势明显',
            '全局高位，BOLL高位，高低波段明显正向，波动率低，反转趋势上转',
            '全局低位，BOLL高位，高低波段明显反向，波动率低，反转趋势上转',
            '全局高位，BOLL高位，高低波段正向明显，波动率低，反转趋势不明显',
            '全局高位，BOLL低位，高低波段负向明显，波动率低，反转趋势不明显',
            '全局低位，BOLL高位，高低波段正向明显，波动率低，反转趋势明显'
            #'全局中位，BOLL低位，高低波段负向明显，波动率较低，反转趋势下转'
        ]

        dict_statement_none=['全局位','BOLL位','高低波段位','波动率','反转趋势']

        order_dict = {
            'trend': None,
            'total unit': total_unit,
            'diff_range': None,
            'method': None,
        }
        if self.status in list_buy and self.last_status not in list_buy:
            print("满足条件:",list_buy[list_buy.index(self.status)],"进行交易")
            log_information="满足条件:"+dict_buy[list_buy.index(self.status)]
            if self.buysell==0:
                self.buysell=1
                self.costprice=self.last_price
                self.profitrate-=self.feerate
                self.realtime_profitrate=self.realtime_profitrate-self.feerate
            else:
                pass
            self.log(log_information)
        elif self.status in list_sell and self.last_status not in list_sell:
            print("满足条件:", list_sell[list_sell.index(self.status)], "进行交易")
            log_information = "满足条件:" + dict_sell[list_sell.index(self.status)]
            if self.buysell == 0:
                self.buysell = -1
                self.costprice = self.last_price
                self.profitrate -= self.feerate
                self.realtime_profitrate = self.realtime_profitrate - self.feerate
            else:
                pass
            self.log(log_information)
        else:
            log_information=''
            print("当前状态:",self.status)
            self.log(log_information)
    def quick_check(self):
        # 持仓时的相对位置
        self.kline = get_last_prices()
        self.last_price=self.kline.closepriceline[len(self.kline.closepriceline)-1]
        log_information = ''
        if self.buysell != 0:
            if (self.last_price - self.shoe) / self.gap >= 1.96 / 3 and self.buysell == -1:  # BOLL线破位
                self.maxmin_status[0] = -1
                self.BOLL_lastingtime_for_deal += 1
            elif (self.last_price - self.shoe) / self.gap <= -1.96 / 3 and self.buysell == 1:
                self.maxmin_status[0] = -1
                self.BOLL_lastingtime_for_deal += 1
            else:
                self.maxmin_status[0] = 0
            if abs((self.last_price - self.costprice) * self.buysell / self.costprice) >= 1000 / 4:  # 止盈止损
                self.maxmin_status[1] = -1
            else:
                self.maxmin_status[1] = 0
            if self.BOLL_lastingtime_for_deal >= 3:
                self.maxmin_status[2] = -1
            else:
                self.maxmin_status[2] = 0
            print(time(), "正在开仓" if self.buysell != 0 else "交易休息中", "仓位数:%d 利润率%f  实时利润率%f,成本价格%f,实时价格%f" % (
            int(self.buysell), self.profitrate,
            self.realtime_profitrate + self.buysell * (self.last_price - self.costprice) / self.costprice,self.costprice,self.last_price), "Infor:",
                  log_information)
        else:
            self.maxmin_status[0] = 0
            self.maxmin_status[1] = 0
            self.maxmin_status[2] = 0
        if self.maxmin_status[2]==-1 or self.maxmin_status[1]==-1:
            log_information='|触发条件平仓|'
            print("触发条件平仓",self.maxmin_status)
            self.buysell = 0
            self.realtime_profitrate = self.realtime_profitrate + (
                        self.last_price - self.costprice) * self.buysell / self.costprice
            self.profitrate = self.realtime_profitrate - self.feerate
        else:
            log_information = ''
            pass
        self.log(log_information)


    def update(self):
        self.kline = get_last_prices()
        self.BOLL = BOLL(self.kline.closepriceline, 1.96)
        ok_min=high_and_low_s(self.kline.closepriceline)
        self.max_min_list = ok_min[1]
        print("最近的非线性阶数:", ok_min[0])
        self.last_price = self.kline.closepriceline[len(self.kline.closepriceline) - 1]
        self.std_line = self.BOLL[3]
        self.upper_sky = self.max_min_list[0][1]
        self.upper_cloud = self.BOLL[0][len(self.BOLL[0]) - 1]
        self.shoe = self.BOLL[1][len(self.BOLL[1]) - 1]
        self.head = self.kline.closepriceline[len(self.kline.closepriceline) - 1]
        self.downer_mud = self.BOLL[2][len(self.BOLL[2]) - 1]
        self.downer_land = self.max_min_list[0][3]

        self.location_global = (self.head - self.downer_land) / (self.upper_sky - self.downer_land)
        self.location_inBOLL = (self.head - self.downer_mud) / (self.upper_cloud - self.downer_mud)

        self.BOLL_level = (self.shoe - self.downer_land) / (self.upper_sky - self.downer_land)

        self.gap = self.std_line[len(self.std_line) - 1]

        self.status = [None, None, None, None,None]
        self.cal_my_status()
        self.judge_mystatus(20)
a=Advanced_Grid()
time_to_update=time()
while True:
    sleep(10)
    if time()-time_to_update>900:
        a.update()
        time_to_update=time()
    else:
        if a.buysell!=0:
            a.quick_check()
        else:
            pass
