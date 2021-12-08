
import numpy as np
from statsmodels.api import OLS
from statsmodels.api import add_constant
from math import log

def EMA(data,N):
    return [2*data[i]*sum([((N-1)/(N+1))**(N-k) for k in range(0,i+1)])/(N+1) for i in range(N,len(data))]
    
def check_nulllist(data):
    for i in data:
        if i==[]:
            return False
    return True

def normalize(data):
    mean=np.mean(data)
    std=np.std(data)
    return [(x-mean)/std for x in data]

def check_timeseries(timeseries):
    lenth=len(timeseries[0])
    for i in timeseries:
        if len(i)==lenth:
            i=i
        else:
            return  False
    return True

def timeserieslength_adjust(timeseries):
    length_list=[len(i) for i in timeseries]
    min_length=min(length_list)
    for i in timeseries:
        while len(i)>min_length:
            del i[0]
    return timeseries

def linear_adjust(data):
    temp_xline=[]
    temp_yline=[]
    ols_params=[]
    add_constant_xline=[]
    for k in range(0,len(data)):
        if data[k] not in [None,np.NaN]:
            temp_xline.append(k)
            temp_yline.append(data[k])
    if temp_xline!=[] and temp_yline!=[]:
        add_constant_xline=add_constant(temp_xline)
        ols_params=OLS(temp_yline,add_constant_xline).fit().params
    for k in range(0,len(data)):
        if data[k]==None or data[k]==np.NaN:
            try:
                data[k]=ols_params[0]+k*ols_params[1]
            except IndexError:
                print("没有值")
                raise IndexError
    return data

def max_min(data):
    M=max(data)
    m=min(data)
    for k in range(0,len(data)):
        data[k]=(data[k]-m)/(M-m)
    return data

def diff(data):
    diff= []
    for k in range(0, len(data)):
        if k == 0:
            diff.append(0)
        else:
            diff.append((data[k] - data[k - 1]))
    return diff

def diff_ratio(data):
    diff_ratio_list=[]
    if len(data)==1:
        return [0]
    else:
        pass
    for k in range(0, len(data)):
        if k == 0:
            diff_ratio_list .append(None)
        else:
            try:
                diff_ratio_list .append((data[k] - data[k - 1])/data[k-1])
            except ZeroDivisionError:
                diff_ratio_list.append(None)
                raise ZeroDivisionError("有错误")
    return linear_adjust(diff_ratio_list)

def log_ratio(data):
    diff_ratio_list = []
    for k in range(0, len(data)):
        if data[k]>0:
            diff_ratio_list.append(log(data[k]))
        else:
            diff_ratio_list.append(None)
    return linear_adjust(diff_ratio_list)

def moving_average(data,params=20):
    if len(data)>params:
        return [np.mean(data[k-20:k]) for k in range(20,len(data))]
    else:
        return  None
def trend_decompose(data):
    xline=[i for i in range(0,len(data))]
    x2line=[i*i for i in range(0,len(data))]
    regress_line=np.array([xline,x2line]).T
    params=OLS(data,add_constant(regress_line)).fit().params
    return [data[i]-i*params[1]-(i**2)*params[2] for i in range(0,len(data))]
    
def panaldata_mean(data):
    returnlist=[]
    if check_timeseries(data)==True:
        for i in range(0,len(data[0])):
            temp_list=[]
            for k in range(0,len(data)):
                temp_list.append(data[k][i])
            returnlist.append(np.mean(temp_list))
        return returnlist
    else:
        data=timeserieslength_adjust(data)
        for i in range(0,len(data[0])):
            temp_list=[]
            for k in range(0,len(data)):
                temp_list.append(data[k][i])
            returnlist.append(np.mean(temp_list))
        return returnlist
        
def check_constant(data):
    non_constant=True
    for i in range(0,len(data)):
        if i==0:
            pass
        else:
            if data[i]==data[i-1]:
                non_constant=False
            else:
                non_constant=True
    return non_constant
    
def check_max_list(data):
    goto=True
    for k in range(0,len(data)-1):
        if data[k]>=data[k+1]:
            pass
        else:
            return False
    return goto

def check_zero_list(data):
    goto=False
    for k in data:
        if k==0:
            return True
        else:
            goto=False
    return goto

def check_all_zero_list(data):
    goto=False
    for k in data:
        if k==0:
            goto=True
        else:
            return False
    return goto

def sort_list_tomin(data):#这里用的冒泡排序
    while check_max_list(data)==False:
        for i in range(0,len(data)-1):
            if data[i]>=data[i+1]:
                pass
            else:
                data[i],data[i+1]=data[i+1],data[i]
    return data