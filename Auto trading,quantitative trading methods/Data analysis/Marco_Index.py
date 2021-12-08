
import Crawler as cr
import DataProcess as dp
import OCR as ocr
import numpy as np
import time
import random
import sklearn.decomposition as skt
import statsmodels.api as sts
import matplotlib.pyplot as mat
timeseries=[]
tis=time.time()
def check_timeseies(timeseries):
    lenth=len(timeseries[0])
    for i in timeseries:
        if len(i)==lenth:
            continue
        else:
            return  False
    return True
def get_indics_all(interval):
    counts=0
    max_count=len(cr.worldindics_yahoo)+len(cr.futures_yahoo)+len(cr.treasury_yahoo)+len(cr.dict_currency_yahoo)
    for i in cr.worldindics_yahoo:
        time.sleep(random.uniform(0, 2))
        close_line = []
        kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
        counts+=1
        print(cr.dict_worldindics_yahoo[i],"finished:",counts*100/max_count,"%")
        timeseries.append(dp.linear_adjust(close_line))
    for i in cr.futures_yahoo:
        close_line = []
        kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
        temp_list = []
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
        counts += 1
        print(cr.dict_futures_yahoo[i],"finished:",counts*100/max_count,"%")
        timeseries.append(dp.linear_adjust(close_line))
    for i in cr.treasury_yahoo:
        close_line = []
        kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
        counts += 1
        print(cr.dict_treasury_yahoo[i],"finished:",counts*100/max_count,"%")
        timeseries.append(dp.linear_adjust(close_line))
    for i in cr.currency_yahoo:
        close_line = []
        kline_result = cr.get_timeseries_result_yahoo(kind=i, interval=interval)
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
        counts += 1
        print(cr.dict_currency_yahoo[i],"finished:",counts*100/max_count,"%")
        timeseries.append(dp.linear_adjust(close_line))
    kline_result=[]
    if check_timeseies(timeseries)==True:
        array_timeseries=np.array(timeseries)
        pca=skt.PCA(n_components=1,whiten=True)
        pca.fit(array_timeseries)
        kline_result = cr.get_timeseries_result_yahoo(kind=cr.main_kind_yahoo[0], interval=interval)
        close_line=[]
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
            print(kline_result[1][l][3])
        main_line=dp.linear_adjust(close_line)
        pca_line=list(pca.mean_)
        newline=[[],[]]
        if len(main_line)!=len(pca_line):
            length_gap=len(main_line)-len(pca_line0)
            if length_gap>0:
                for i in range(0,min(len(main_line,len(pca_line)))):
                    newline[0].append(main_line[i+length_gap-1],pca_line[i])
            else:
                for i in range(0,min(len(main_line,len(pca_line)))):
                    newline[0].append(main_line[i],pca_line[i+length_gap-1])
        ols_result=sts.OLS(main_line,pca_line).fit()
        std_param=ols_result.params[0]/ols_result.tvalues[0]
        previous_index_line=[(main_line[i]/pca_line[i]-ols_result.params[0])/std_param for i in range(0,len(pca_line))]
        normal_line=dp.normalize(main_line)
        print(len(main_line),len(pca_line))
        print(ols_result.summary())
        return [normal_line,previous_index_line,main_line,pca_line]
    else:
        min_lenth=0
        for i in range(0,len(timeseries)):
            if len(timeseries[i])<len(timeseries[i+1]) and i!=len(timeseries)-1:
                min_lenth=len(timeseries[i])
            elif i==len(timeseries)-1:
                min_lenth=len(timeseries[i])
            else:
                min_lenth=min_lenth
        for i in range(0,len(timeseries)):
            while len(i)>=min_lenth:
                del timeseries[i][0]
        array_timeseries = np.array(timeseries)
        pca = skt.PCA(n_components=1, whiten=True)
        pca.fit(array_timeseries)
        kline_result = cr.get_timeseries_result_yahoo(kind=cr.main_kind_yahoo[0], interval=interval)
        close_line = []
        for l in range(0, len(kline_result[0])):
            close_line.append(kline_result[1][l][3])
            print(kline_result[1][l][3])
        main_line = dp.linear_adjust(close_line)
        pca_line = list(pca.components_)
        newline = [[], []]
        if len(main_line) != len(pca_line):
            length_gap = len(main_line) - len(pca_line0)
            if length_gap > 0:
                for i in range(0, min(len(main_line, len(pca_line)))):
                    newline[0].append(main_line[i + length_gap - 1], pca_line[i])
            else:
                for i in range(0, min(len(main_line, len(pca_line)))):
                    newline[0].append(main_line[i], pca_line[i + length_gap - 1])
        ols_result = sts.OLS(main_line, pca_line).fit()
        std_param = ols_result.params[0] / ols_result.tvalues[0]
        previous_index_line = [(main_line[i] / pca_line[i] - ols_result.params[0]) / std_param for i in
                               range(0, len(pca_line))]
        normal_line = dp.normalize(main_line)
        print(len(main_line), len(pca_line))
        print(ols_result.summary())
        return [normal_line, previous_index_line, main_line, pca_line]
test_result=get_indics_all('15m')
print("--------------------------------------------------------")
for i in range(0,len(test_result[0])):
    print(test_result[0][i],test_result[1][i],test_result[2][i],test_result[3][i])
now_time=time.time()
x_line=[now_time-x*60*60 for x in range(0,len(test_result[0]))]
mat.plot(x_line,test_result[0])
mat.plot(x_line,test_result[1])
mat.show()