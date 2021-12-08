import okex.client as cli
import statsmodels.api as sm
import numpy as np
import math
import time
import requests
import urllib3
import csv
from matplotlib import pyplot as plt
con=True
def backfunc(shuzu):
    kk=[]
    kk.append(0)
    for t in range(1,len(shuzu)-1):
        kk.append(shuzu[t])
    kk.append(kk[len(kk)-1])
    return kk
culprofit=0
culadprofit=0
def bodong(pricelist):
    return (abs(pricelist[len(pricelist)-1]-pricelist[len(pricelist)-2])+abs(pricelist[len(pricelist)-2]-pricelist[len(pricelist)-3]))/2
def opfunc(profitline,positionline):
    tempa=-10
    ratiolist=[]
    alist=[]
    asqlist=[]
    avelist=[]
    stdlist=[]
    logratio=[]
    weightnum=0
    for i in range(0, len(positionline) - 1):
        weightnum += (math.exp(i * 3 / len(positionline))-1)
    while tempa<=-0.01:
        tempprofit=0
        tempprofit2=0
        stdtemp2=0
        stdtemp=0
        alist.append(tempa)
        asqlist.append(tempa**2)
        for i in range(0,len(positionline)-1):
            testposition=positionline[i]*tempa
            tempprofit+=profitline[i]*(testposition/positionline[i])*(math.exp(i*3/len(positionline))-1)
            tempprofit2+=profitline[i]*(testposition/positionline[i])
        for k in range(0, len(positionline) - 1):
            testposition = positionline[k] *tempa
            stdtemp+=((profitline[k]*(testposition/positionline[k])-tempprofit/len(positionline))**2)*(math.exp(k*3/len(positionline))-1)
            stdtemp2+=((profitline[k]*(testposition/positionline[k])-tempprofit/len(positionline))**2)
        ave=tempprofit/weightnum
        ave2=tempprofit2/len(profitsline)
        avelist.append(ave/2+ave2/2)
        std=math.sqrt(stdtemp/weightnum)
        std2=math.sqrt(stdtemp2/len(profitsline))
        stdlist.append(std/2+std2/2)
        ratiolist.append((ave/2+ave2/2)**3/math.exp(std/2+std2/2))



        tempa+=0.01
    tempa = 0.01
    alist.append(0.00)
    asqlist.append(0.00)

    ratiolist.append(0)
    avelist.append(0.00000000000000000000000)
    stdlist.append(0.00000000000000000000000)
    while tempa <= 10:
        tempprofit = 0
        tempprofit2 = 0
        stdtemp2 = 0
        stdtemp = 0
        alist.append(tempa)
        asqlist.append(tempa ** 2)
        for i in range(0, len(positionline) - 1):
            testposition = positionline[i] * tempa
            tempprofit += profitline[i] * (testposition / positionline[i]) * (math.exp(i * 3 / len(positionline)) - 1)
            tempprofit2 += profitline[i] * (testposition / positionline[i])
        for k in range(0, len(positionline) - 1):
            testposition = positionline[k] * tempa
            stdtemp += ((profitline[k] * (testposition / positionline[k]) - tempprofit / len(positionline)) ** 2) * (
                        math.exp(k * 3 / len(positionline)) - 1)
            stdtemp2 += ((profitline[k] * (testposition / positionline[k]) - tempprofit / len(positionline)) ** 2)
        ave = tempprofit / weightnum
        ave2 = tempprofit2 / len(profitsline)
        avelist.append(ave / 2 + ave2 / 2)
        std = math.sqrt(stdtemp / weightnum)
        std2 = math.sqrt(stdtemp2 / len(profitsline))
        stdlist.append(std / 2 + std2 / 2)
        ratiolist.append((ave / 2 + ave2 / 2) ** 3 / math.exp(std / 2 + std2 / 2))

        tempa += 0.01

    print("最优thea值为", -10 + np.argmax(ratiolist) * 0.01, "其利润均值为", avelist[np.argmax(ratiolist)], "其利润标准差为:",
              stdlist[np.argmax(ratiolist)])
    return -10 + np.argmax(ratiolist) * 0.01

def judgeposition(pre,price):
    if pre>price:
        return 1
    elif pre==price:
        return 0
    else:
        return -1
def calprofit(position,prilast,pripre):

    if position==0:
        return 0
    elif position>0:
        if prilast>pripre:
            return position*(prilast-pripre)
        else:
            return position * (prilast - pripre)
    else:
        if prilast>pripre:
            return position*(prilast-pripre)
        else:
            return position * (prilast - pripre)


api_keys=""
secretkey=""
password=""
spot_price=[]
future_price=[]
ltc_spot=[]
predict_price=[]
dx=cli.Client(api_key=api_keys,api_seceret_key=secretkey,passphrase=password)

btckx_results=dx._request_without_params(method="GET",request_path="/api/spot/v3/instruments/BTC-USDT/candles?granularity=180")
btcfukx_results=dx._request_without_params(method="GET",request_path="/api/swap/v3/instruments/BTC-USD-SWAP/candles?granularity=180")
ltckx_results=dx._request_without_params(method="GET",request_path="/api/spot/v3/instruments/LTC-USDT/candles?granularity=180")
profitsline=[]
positionsline=[]
for i in range(0,len(btckx_results)-1):
    spot_price.append(float(btckx_results[len(btckx_results)-1-i][4]))
    future_price.append(float(btcfukx_results[len(btckx_results)-1-i][4]))
    ltc_spot.append((float(ltckx_results[len(ltckx_results)-1-i][4])))
new_column=sm.add_constant(np.column_stack((backfunc(future_price),backfunc(spot_price),backfunc(ltc_spot))))
ors=sm.OLS(future_price,new_column).fit().params
for k in range(0,len(future_price)-1):
    predict_price.append(ors[0]+ors[1]*backfunc(future_price)[k]+ors[2]*backfunc(spot_price)[k]+ors[3]*backfunc(ltc_spot)[k])
    positionsline.append(judgeposition(predict_price[k],future_price[k]))
    if k==len(future_price)-1:
        btcswap_results_temp = dx._request_without_params(method="GET",
                                                     request_path="/api/swap/v3/instruments/BTC-USD-SWAP/ticker")
        profitsline.append(calprofit(positionsline[k], (float(btcswap_results_temp['last']), future_price[k])))
    else:
        profitsline.append(calprofit(positionsline[k],future_price[k+1],future_price[k]))
print("基础数据准备完毕，损失函数为ave3-expstd型，Final-Test")


def jiaoyi():
    global culadprofit,culprofit
    try:
        temp_bodong = bodong(future_price)
        if temp_bodong >=0:
            # if bodong(future_price) >= 0:

            btcswap_results = dx._request_without_params(method="GET",
                                                         request_path="/api/swap/v3/instruments/BTC-USD-SWAP/ticker")
            future_price.append(float(btcswap_results['last']))
            btcspot_results = dx._request_without_params(method="GET",
                                                         request_path="/api/spot/v3/instruments/BTC-USDT/ticker")
            spot_price.append(float(btcspot_results['last']))
            ltcspot_results = dx._request_without_params(method="GET",
                                                         request_path="/api/spot/v3/instruments/LTC-USDT/ticker")
            ltc_spot.append(float(ltcspot_results['last']))
            print("-------------------------------------------------------------------------------")
            top = opfunc(profitsline, positionsline)
            new_column_2 = sm.add_constant(
                np.column_stack((backfunc(future_price), backfunc(spot_price), backfunc(ltc_spot))))
            print("拟合程度：", sm.OLS(future_price, new_column_2).fit().rsquared_adj, "最新价:",
                  float(btcswap_results['last']))
            print("波动率充足,开始交易,波动率:", temp_bodong)
            new_column = sm.add_constant(
                np.column_stack((backfunc(future_price), backfunc(spot_price), backfunc(ltc_spot))))
            ors = sm.OLS(future_price, new_column).fit().params
            predict_price.append(ors[0] + ors[1] * backfunc(future_price)[len(future_price) - 1] +
                                 ors[2] * backfunc(spot_price)[len(spot_price) - 1] +
                                 ors[3] * backfunc(ltc_spot)[len(ltc_spot) - 1])
            positionsline.append(
                judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]))
            profitsline.append(calprofit(positionsline[len(positionsline) - 2], future_price[len(future_price) - 1],
                                         future_price[len(future_price) - 2]))
            culprofit += calprofit(
                judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]),
                future_price[len(future_price) - 1], future_price[len(future_price) - 2])
            print("判断仓位方向为:", judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]),
                  "利润为:",
                  calprofit(judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]),
                            future_price[len(future_price) - 1], future_price[len(future_price) - 2]),
                  "累计利润为:", culprofit)

            if top == 0:
                tposition = 0
            else:

                tposition = judgeposition(predict_price[len(predict_price) - 1],
                                          future_price[len(future_price) - 1]) * top
            culadprofit += calprofit(tposition,
                                     future_price[len(future_price) - 1], future_price[len(future_price) - 2])
            datass = float(btcswap_results['last']), judgeposition(predict_price[len(predict_price) - 1],
                                                                   future_price[len(future_price) - 1]), calprofit(
                judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]),
                future_price[len(future_price) - 1],
                future_price[len(future_price) - 2]), culprofit, tposition, culadprofit
            print("调整仓位方向为:", tposition,
                  "利润为：", calprofit(tposition,
                                    future_price[len(future_price) - 1], future_price[len(future_price) - 2]),
                  "累计利润为:", culadprofit)
            with open("C-D-expikfunc.csv", 'a', newline='') as fl:
                f_csv = csv.writer(fl)
                f_csv.writerow(datass)
        else:
            print("-------------------------------------------------------------------------------")
            print("波动率不足,停止交易,波动率:", temp_bodong)
            top = opfunc(profitsline, positionsline)
            btcswap_results = dx._request_without_params(method="GET",
                                                         request_path="/api/swap/v3/instruments/BTC-USD-SWAP/ticker")
            future_price.append(float(btcswap_results['last']))
            btcspot_results = dx._request_without_params(method="GET",
                                                         request_path="/api/spot/v3/instruments/BTC-USDT/ticker")
            spot_price.append(float(btcspot_results['last']))
            ltcspot_results = dx._request_without_params(method="GET",
                                                         request_path="/api/spot/v3/instruments/LTC-USDT/ticker")
            ltc_spot.append(float(ltcspot_results['last']))

            new_column = sm.add_constant(
                np.column_stack((backfunc(future_price), backfunc(spot_price), backfunc(ltc_spot))))
            ors = sm.OLS(future_price, new_column).fit().params
            print("拟合程度：", sm.OLS(future_price, new_column).fit().rsquared_adj, "最新价:", float(btcswap_results['last']))
            predict_price.append(ors[0] + ors[1] * backfunc(future_price)[len(future_price) - 1] +
                                 ors[2] * backfunc(spot_price)[len(spot_price) - 1] +
                                 ors[3] * backfunc(ltc_spot)[len(ltc_spot) - 1])
            positionsline.append(
                judgeposition(predict_price[len(predict_price) - 1], future_price[len(future_price) - 1]))
            profitsline.append(0)

        time.sleep(168)
    except  requests.exceptions.ProxyError:
        print("-------------------------------------------------------------------------------")
        print("网络错误")
        jiaoyi()

    except OSError:
        print("-------------------------------------------------------------------------------")
        print("网络错误")
        jiaoyi()

    except urllib3.exceptions.MaxRetryError:
        print("-------------------------------------------------------------------------------")
        print("网络错误")
        jiaoyi()


    except ValueError as e:
        print("-------------------------------------------------------------------------------")
        print("计算错误")
        lensgp=[len(future_price),len(spot_price),len(ltc_spot)]
        if np.argmin(lensgp)==0:
            future_price.append(np.average(future_price[lensgp[0]-4:lensgp[0]]))
            spot_price.append(np.average(spot_price[lensgp[0]-4:lensgp[0]]))
            ltc_spot.append(np.average(ltc_spot[lensgp[0]-4:lensgp[0]]))
        elif np.argmin(lensgp)==1:
            spot_price.append(np.average(spot_price[lensgp[0] - 4:lensgp[0]]))
            ltc_spot.append(np.average(ltc_spot[lensgp[0] - 4:lensgp[0]]))
        else:
            ltc_spot.append(np.average(ltc_spot[lensgp[0] - 4:lensgp[0]]))
        jiaoyi()


while con==True:
    jiaoyi()

