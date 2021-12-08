# coding=UTF-8
from csv import reader,writer
from numpy import array,mean,std,log as numpy_log,cov,ones,inf
from random import randint,sample,normalvariate
from pandas import read_csv
from sklearn import linear_model,svm,naive_bayes,tree,neighbors,neural_network,ensemble
from numpy.linalg import inv
from scipy.optimize import minimize,Bounds,basinhopping
#from LogisticModel_up2 import Logistic_signal
from matplotlib.pyplot import plot,show,subplot,ylabel
import pandas.errors
from math import log,exp,pi,sin,cos,sqrt
from scipy.optimize import basinhopping,minimize_scalar
from statsmodels.api import OLS,add_constant
from keras.models import Sequential,Model,Input
from keras.layers import LSTM,Embedding,Dropout,Dense
from keras.optimizers import SGD,Adam
from keras.utils.np_utils import to_categorical
from talib import RSI,BBANDS
from time import time
import os
from random import uniform
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
lc_ratio=1
trade_cost=float(0.0005)
norisk_yield=0.0234
closest_3 = lambda x: int([abs(x + 1),abs(x), abs(x - 1)].index(min([abs(x + 1),abs(x), abs(x - 1)])))-1
to_list=lambda x :float(x)
def corr(x,y):
    return cov(array(x),array(y))[0][1]/(std(x)*std(y))
def closet_3_single(x):

    if x > 1 / 3:
        return 1
    elif x < -1 / 3:
        return -1
    else:
        return 0
def tag_signal(close,param_S):
    tag_list = [{
        '-4': 0,
        '-3': 0,
        '-2': 0,
        '-1': 0,
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    } for i in range(0, len(close))]
    for i in range(0, len(close) - param_S - 1, param_S):

        temp_list = close[i:i + param_S]
        index_max = temp_list.index(max(temp_list))
        index_min = temp_list.index(min(temp_list))
        if (max(temp_list) - min(temp_list)) / min(temp_list) > trade_cost:
            if index_max < index_min:

                if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                    tag_list[i]['2'] += 1
                    tag_list[i + index_max]['-3'] += 1
                else:
                    tag_list[i]['0'] += 1
                    tag_list[i + index_max]['-2'] += 1
                for j in range(1, index_max):

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                        tag_list[i + j]['3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1

                for j in range(index_max, index_min):
                    tag_list[i + j]['-4'] += 1

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + index_min]['4'] += 1
                else:
                    tag_list[i + index_min]['-1'] += 1

                for j in range(index_min + 1, param_S):
                    if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                        tag_list[i + j]['3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #
                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                    tag_list[i + param_S]['1'] += 1
                else:
                    tag_list[i + param_S]['0'] += 1

            else:

                if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                    tag_list[i]['-2'] += 1
                    tag_list[i + index_min]['3'] += 1

                else:
                    tag_list[i]['0'] += 1
                    tag_list[i + index_min]['2'] += 1

                for j in range(1, index_min):

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                        tag_list[i + j]['-3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #
                for j in range(index_min + 1, index_max):
                    tag_list[i + j]['4'] += 1
                #

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + index_min]['-4'] += 1
                else:
                    tag_list[i + index_min]['1'] += 1
                #
                for j in range(index_min + 1, param_S):

                    if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                        tag_list[i + j]['-3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + param_S]['-1'] += 1
                else:
                    tag_list[i + param_S]['0'] += 1
        else:
            #
            for j in range(0, param_S):
                tag_list[i + j]['0'] += 1
    tagged_line = [None for i in tag_list]
    do_or_notdo = [None for i in tag_list]
    buy_or_sell = [None for i in tag_list]
    continues_signal = [float(0) for i in tag_list]
    finalsignal_list = []
    for reading_tag in range(0, len(tag_list)):
        signal = []

        for k in tag_list[reading_tag].keys():
            if tag_list[reading_tag][k] != 0:
                signal.append([int(k), tag_list[reading_tag][k]])
        if len(signal) == 1:
            final_signal = None
            finalsignal_list.append(signal[0][0] if signal[0][0] not in [-4, 4] else 0)
            continues_signal[reading_tag] = signal[0][0]
            if signal[0][0] == 0:
                final_signal = 0
            elif signal[0][0] > 0:
                final_signal = 1
            else:
                final_signal = -1
            tagged_line[reading_tag] = final_signal
            if final_signal in [-4, 4]:
                do_or_notdo[reading_tag] = 0
            else:
                do_or_notdo[reading_tag] = 1 if final_signal != 0 else 0  # #
            if final_signal == 0:
                buy_or_sell[reading_tag] = None
            elif final_signal > 0:
                buy_or_sell[reading_tag] = 1
            else:
                buy_or_sell[reading_tag] = -1
        else:
            total_value = 0
            for i in signal:
                total_value += i[0] / len(signal)
            continues_signal[reading_tag] = total_value / 8
            final_signal = None
            finalsignal_list.append(round(total_value) if round(total_value) not in [-4, 4] else 0)
            if round(total_value) == 0:
                final_signal = 0
            elif round(total_value) > 0:
                final_signal = 1
            else:
                final_signal = -1
            tagged_line[reading_tag] = final_signal
            if final_signal in [-4, 4]:
                do_or_notdo[reading_tag] = 0
            else:
                do_or_notdo[reading_tag] = 1 if final_signal != 0 else 0  # #
            if final_signal == 0:
                buy_or_sell[reading_tag] = None
            elif final_signal > 0:
                buy_or_sell[reading_tag] = 1
            else:
                buy_or_sell[reading_tag] = -1
    anotherbuysellsignal = [0 if buy_or_sell[i] == None else buy_or_sell[i] for i in
                                 range(buy_or_sell.__len__())]
    return [do_or_notdo,anotherbuysellsignal]
def tag_signal_continuous(close,param_S,trade_cost=0.001):
    tag_list = [{
        '-4': 0,
        '-3': 0,
        '-2': 0,
        '-1': 0,
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    } for i in range(0, len(close))]
    for i in range(0, len(close) - param_S - 1, param_S):

        temp_list = close[i:i + param_S]
        index_max = temp_list.index(max(temp_list))
        index_min = temp_list.index(min(temp_list))
        if (max(temp_list) - min(temp_list)) / min(temp_list) > trade_cost:
            if index_max < index_min:

                if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                    tag_list[i]['2'] += 1
                    tag_list[i + index_max]['-3'] += 1
                else:
                    tag_list[i]['0'] += 1
                    tag_list[i + index_max]['-2'] += 1
                for j in range(1, index_max):

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                        tag_list[i + j]['3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1

                for j in range(index_max, index_min):
                    tag_list[i + j]['-4'] += 1

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + index_min]['4'] += 1
                else:
                    tag_list[i + index_min]['-1'] += 1

                for j in range(index_min + 1, param_S):
                    if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                        tag_list[i + j]['3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #
                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                    tag_list[i + param_S]['1'] += 1
                else:
                    tag_list[i + param_S]['0'] += 1

            else:

                if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                    tag_list[i]['-2'] += 1
                    tag_list[i + index_min]['3'] += 1

                else:
                    tag_list[i]['0'] += 1
                    tag_list[i + index_min]['2'] += 1

                for j in range(1, index_min):

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost:
                        tag_list[i + j]['-3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #
                for j in range(index_min + 1, index_max):
                    tag_list[i + j]['4'] += 1
                #

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + index_min]['-4'] += 1
                else:
                    tag_list[i + index_min]['1'] += 1
                #
                for j in range(index_min + 1, param_S):

                    if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:

                        tag_list[i + j]['-3'] += 1
                    else:
                        tag_list[i + j]['0'] += 1
                #

                if (temp_list[param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost:
                    tag_list[i + param_S]['-1'] += 1
                else:
                    tag_list[i + param_S]['0'] += 1
        else:
            #
            for j in range(0, param_S):
                tag_list[i + j]['0'] += 1
    continues_signal = [float(0) for i in tag_list]
    for reading_tag in range(0, len(tag_list)):
        signal = []
        for k in tag_list[reading_tag].keys():
            if tag_list[reading_tag][k] != 0:
                signal.append([int(k), tag_list[reading_tag][k]])
        if len(signal) == 1:
            continues_signal[reading_tag] = signal[0][0]/4
        else:
            total_value = 0
            for i in signal:
                total_value += i[0] / len(signal)
            continues_signal[reading_tag] = total_value / 4
    return continues_signal
def avoid_null(data_list):
    new_list=[]
    for i in range(0,len(data_list)):
        if data_list[i]!=None:
            new_list.append(data_list[i])
    return new_list
def max_min(data_list,max,min):
    new_list=[]
    for i in range(0,len(data_list)):
        new_list.append((data_list[i]-min)/(max-min))
    return new_list
def test_max_min(data_list,max_val,min_val):
    new_list = []
    for i in range(0, len(data_list)):
        new_list.append((data_list[i] -min_val) / (max_val - min_val))
    return new_list
def cal_profitrate(pricelist,signallist,plotornot=False,timeline=None,**judge_model):

    i = 0
    each_tragy_diffratio = []
    each_long_diffratio = []
    for j in range(1, len(pricelist)):
        each_tragy_diffratio.append((pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
        each_long_diffratio.append(signallist[j] * (pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
    i = 0
    profitrate = 1
    list_profitrate = [0]
    times = 0
    each_order_yield=[]
    culmulative_profitrate = []
    while i < len(signallist) - 2:
        trend=None
        cost_price=None
        if signallist[i] != 0:
            print("-" * 168)
            print("open order at", timeline[i], "trend at", signallist[i])
            trend = signallist[i]
            cost_price = pricelist[i]
            if i + 1 < len(signallist) - 1:

                while signallist[i + 1] != 0 and signallist[i + 1] == trend:
                    if i < len(signallist) - 2:
                        culmulative_profitrate.append(
                            profitrate+(trend * float(pricelist[i] - cost_price) / cost_price - trade_cost*(1+pricelist[i]/cost_price)))
                        i += 1
                    else:
                        profitrate += (
                                trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price -trade_cost*(1+pricelist[len(pricelist) - 1]/cost_price))
                        list_profitrate.append(
                            profitrate)
                        culmulative_profitrate.append(profitrate +(trend * float(
                            pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost))
                        each_order_yield.append(trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost*(1+pricelist[len(pricelist) - 1]/cost_price))
                        print("this profit rate",trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost*(1+pricelist[len(pricelist) - 1]/cost_price))
                        print("close order at", timeline[i])
                        times += 1
                        break
                else:
                    if trend != None:
                        i += 1
                        profitrate += (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                        list_profitrate.append(profitrate)
                        culmulative_profitrate.append(
                            profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                        each_order_yield.append((trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                        print("this profit rate",trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                        print("close order at", timeline[i])
                        times += 1
                    else:
                        print("pass")
            else:
                break
        else:
            culmulative_profitrate.append(
                profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost) if trend!=None else profitrate)
            list_profitrate.append(
                profitrate)
            i += 1
    subplot(3,1,1)
    plot([i for i in range(len(culmulative_profitrate))],culmulative_profitrate)
    subplot(3,1,2)
    plot([i for i in range(len(list_profitrate))], list_profitrate)
    subplot(3, 1, 3)
    plot([i for i in range(len(culmulative_profitrate))], pricelist[:len(culmulative_profitrate)])
    show()

    sigma = std(each_tragy_diffratio)
    highest_in_min = max(culmulative_profitrate[:culmulative_profitrate.index(min(culmulative_profitrate)) + 1])
    lowest_cul_profitrate = min(culmulative_profitrate)
    max_retreat = (lowest_cul_profitrate - highest_in_min) / highest_in_min if highest_in_min != 0 else 0
    sharp_ratio = (profitrate - 1 -norisk_yield*len(pricelist)/(365*12*24)) / (sigma*sqrt((365*12*24))) if sigma > 0 else 0
    calmar_ratio = (profitrate - 1 -norisk_yield*len(pricelist)/(365*5*24)) / abs(max_retreat) if max_retreat < 0 else 0
    CAPM_resultr = OLS(each_tragy_diffratio, add_constant(array(each_long_diffratio).T)).fit()
    max_order_loss=min(each_order_yield)
    G_calmar_ratio=(profitrate - 1 - norisk_yield*len(pricelist)/(365*5*24)) / abs(max_order_loss) if max_order_loss<0 else 1e+234
    print(CAPM_resultr.summary())
    alpha = CAPM_resultr.params[0]*365*24*12
    beta = CAPM_resultr.params[1]
    print("----------Summary---------")
    print("Profit rate:",profitrate-1)
    print("Sigma:",sigma)
    print("Max retreat:",max_retreat)
    print("Sharp ratio:",sharp_ratio)
    print("Calmar ratio:",calmar_ratio)
    print("Generalized calmar_ratio",G_calmar_ratio)
    print("Max order yield loss",max_order_loss)
    print("Alpha:",alpha)
    print("Beta:",beta)

    return -(2.5559653367102384 * profitrate -
             30391.887967016268 * sigma -
             1.7226895022326197e-06 * max_retreat +
             2285.6531545522867 * calmar_ratio +
             0.0013132050693759382 * sharp_ratio +
             10898507.741068777 * alpha +
             0.0037153588718620203 * times
             - ((beta) * 38.496196762272554) ** 2)
def weight_indicators(pricelist):
    repeat=float(0)
    profit_list=[]
    sigma_list= []
    max_retreat_list =[]
    sharp_ratio_list =[]
    calmar_ratio_list =[]
    alpha_list = []
    beta_list=[]

    while repeat<=100:
        signallist = []
        each_tragy_diffratio = []
        each_long_diffratio = []
        for j in range(1, len(pricelist)):
            random_sample = randint(-1, 1)
            signallist.append(random_sample)
            each_tragy_diffratio.append((pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
            each_long_diffratio.append(random_sample * (pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
        each_tragy_diffratio = []
        each_long_diffratio = []
        for j in range(1, len(pricelist)):
            each_tragy_diffratio.append((pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
            each_long_diffratio.append(signallist[j-1] * (pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
        i = 0
        profitrate = float(1)
        list_profitrate = []
        times = float(0)
        culmulative_profitrate = []
        while i < len(signallist) - 2:
            trend=None
            cost_price=None
            if signallist[i] != 0:
                trend = signallist[i]
                cost_price = pricelist[i]
                if i + 1 < len(signallist) - 1:
                    while signallist[i + 1] != 0 and signallist[i + 1] == trend:
                        if i < len(signallist) - 2:
                            culmulative_profitrate.append(
                                profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                            i += 1
                        else:
                            profitrate += (
                                    trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                            list_profitrate.append(
                                trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                            culmulative_profitrate.append(profitrate + trend * float(
                                pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                            times += 1
                            break
                    else:
                        if trend != None:
                            i += 1
                            profitrate += (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                            list_profitrate.append(trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                            culmulative_profitrate.append(
                                profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                            times += 1
                        else:
                            print("pass")
                else:
                    break
            else:
                culmulative_profitrate.append(
                    profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)if trend!=None else profitrate)
                i += 1
        sigma = std(each_tragy_diffratio)
        highest_in_min = max(culmulative_profitrate[:culmulative_profitrate.index(min(culmulative_profitrate)) + 1])
        lowest_cul_profitrate = min(culmulative_profitrate)
        max_retreat = (lowest_cul_profitrate - highest_in_min) / highest_in_min
        sharp_ratio = (profitrate - 1 - 0.0385) / sigma if sigma > 0 else 0
        calmar_ratio = (profitrate - 1 - 0.0385) / abs(max_retreat) if max_retreat < 0 else 0
        CAPM_resultr = OLS(each_tragy_diffratio, add_constant(array(each_long_diffratio).T)).fit()
        print(CAPM_resultr.summary())
        alpha = CAPM_resultr.params[0]
        beta = CAPM_resultr.params[1]
        profit_list.append(profitrate)
        sigma_list.append(sigma)
        max_retreat_list.append(max_retreat)
        sharp_ratio_list.append(sharp_ratio)
        calmar_ratio_list .append(calmar_ratio)
        alpha_list.append(alpha)
        beta_list.append(beta)
        repeat+=1
        print(repeat/100)
    print("profit_list mean",mean(profit_list),"std",std(profit_list),"weight",1/std(profit_list))
    print("sigma_list mean",mean(sigma_list),"std",std(sigma_list),"weight",1/std(sigma_list))
    print("max_retreat_list mean",mean(max_retreat_list),"std",std(max_retreat_list),"weight",1/std(max_retreat_list))
    print("sharp_ratio_list mean",mean(sharp_ratio_list),"std",std(sharp_ratio_list),"weight",1/std(sharp_ratio_list))
    print("calmar_ratio_list mean",mean(calmar_ratio_list),"std",std(calmar_ratio_list),"weight",1/std(calmar_ratio_list))
    print("alpha_list mean",mean(alpha_list),"std",std(alpha_list),"weight",1/std(alpha_list))
    print("beta_list mean",mean(beta_list),"std",std(beta_list),"weight",1/std(beta_list))
def opt_calprofitrate(pricelist,beta_vector,factor_matrix):
    signallist=[]
    param_k=24
    closest_3=lambda x:int(float([abs(x+1),abs(x-1)].index(min([abs(x+1),abs(x-1)]))-0.5)*2)#
    #closest=lambda x:[abs(x-beta_vector[0]),abs(x-beta_vector[1]),abs(x-beta_vector[2])].index(min([abs(x-beta_vector[0]),abs(x-beta_vector[1]),abs(x-beta_vector[2])]))-1
    tanh=lambda x:1 if x>0 else -1
    sigmoid=lambda x:1 if x>0 else 0
    for j in range(len(pricelist)):
        xi=array(factor_matrix[j]).dot(beta_vector[:(len(beta_vector)-param_k)/2])
        alpha=array(factor_matrix[j]).dot(beta_vector[(len(beta_vector)-param_k)/2:(len(beta_vector)-param_k)])
        for k in range(0,param_k):
            alpha+=beta_vector[len(beta_vector)-param_k-1+k]*sigmoid(xi)
        signallist.append(float(sigmoid(xi)) * tanh(alpha))
    each_tragy_diffratio = []
    each_long_diffratio = []
    for j in range(1, len(pricelist)):
        each_tragy_diffratio.append((pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
        each_long_diffratio.append(signallist[j] * (pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
    i = 0
    profitrate=float(1)
    list_profitrate = []
    times = float(0)
    culmulative_profitrate = []
    while i < len(signallist) - 2:
        trend=None
        cost_price=None
        if signallist[i] != 0:
            trend = signallist[i]
            cost_price = pricelist[i]
            if i + 1 < len(signallist) - 1:
                while signallist[i + 1] != 0 and signallist[i + 1] == trend:
                    if i < len(signallist) - 2:
                        culmulative_profitrate.append(
                            profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                        i += 1
                    else:
                        profitrate += (
                                trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                        list_profitrate.append(
                            trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                        culmulative_profitrate.append(profitrate+trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost)
                        times += 1
                        break
                else:
                    if trend != None:
                        i += 1
                        profitrate += (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                        list_profitrate.append(trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                        culmulative_profitrate.append(profitrate+ (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                        times += 1
                    else:
                        print("pass")
            else:
                break
        else:
            culmulative_profitrate.append(
                profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost) if trend!=None else profitrate)
            list_profitrate.append(trend * float(pricelist[i] - cost_price) / cost_price - trade_cost if trend!=None else 0)
            i += 1
    sigma = std(each_tragy_diffratio)
    highest_in_min = max(culmulative_profitrate[:culmulative_profitrate.index(min(culmulative_profitrate)) + 1])
    lowest_cul_profitrate = min(culmulative_profitrate)
    max_retreat = (lowest_cul_profitrate-highest_in_min  ) / highest_in_min if highest_in_min!=0 else 0
    sharp_ratio = (profitrate - 1 - 0.15) / sigma if sigma>0 else 0
    calmar_ratio = (profitrate - 1 - 0.15) / abs(max_retreat) if max_retreat<0 else 0
    CAPM_resultr = OLS(each_tragy_diffratio, add_constant(array(each_long_diffratio).T)).fit()

    alpha = CAPM_resultr.params[0]
    beta = CAPM_resultr.params[1]
    return -(2.5559653367102384 * profitrate -
             30391.887967016268 * sigma -
             1.7226895022326197e-06 * max_retreat +
             2285.6531545522867 * calmar_ratio +
             0.0013132050693759382 * sharp_ratio +
             10898507.741068777 * alpha +
             0.0037153588718620203 * times
             - ((beta - 0.5) * 38.496196762272554) ** 2)
def cal_profitfunc_noprint(pricelist,signallist):
    i = 0
    each_tragy_diffratio = []
    each_long_diffratio = []
    for j in range(1, len(pricelist)):
        each_tragy_diffratio.append((pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
        each_long_diffratio.append(signallist[j] * (pricelist[j] - pricelist[j - 1]) / pricelist[j - 1])
    i = 0
    profitrate = 1
    list_profitrate = [0]
    times = 0
    each_order_yield=[]
    culmulative_profitrate = []
    while i < len(signallist) - 2:
        trend=None
        cost_price=None
        if signallist[i] != 0:
            trend = signallist[i]
            cost_price = pricelist[i]
            if i + 1 < len(signallist) - 1:

                while signallist[i + 1] != 0 and signallist[i + 1] == trend:
                    if i < len(signallist) - 2:
                        culmulative_profitrate.append(
                            profitrate+(trend * float(pricelist[i] - cost_price) / cost_price - trade_cost*(1+pricelist[i]/cost_price)))
                        i += 1
                    else:
                        profitrate += (
                                trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price -trade_cost*(1+pricelist[len(pricelist) - 1]/cost_price))
                        list_profitrate.append(
                            profitrate)
                        culmulative_profitrate.append(profitrate +(trend * float(
                            pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost))
                        each_order_yield.append(trend * float(pricelist[len(pricelist) - 1] - cost_price) / cost_price - trade_cost*(1+pricelist[len(pricelist) - 1]/cost_price))

                        times += 1
                        break
                else:
                    if trend != None:
                        i += 1
                        profitrate += (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost)
                        list_profitrate.append(profitrate)
                        culmulative_profitrate.append(
                            profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))
                        each_order_yield.append((trend * float(pricelist[i] - cost_price) / cost_price - trade_cost))

                        times += 1
                    else:
                        pass
            else:
                break
        else:
            culmulative_profitrate.append(
                profitrate + (trend * float(pricelist[i] - cost_price) / cost_price - trade_cost) if trend!=None else profitrate)
            list_profitrate.append(
                profitrate)
            i += 1


    sigma = std(each_tragy_diffratio)
    highest_in_min = max(culmulative_profitrate[:culmulative_profitrate.index(min(culmulative_profitrate)) + 1])
    lowest_cul_profitrate = min(culmulative_profitrate)
    max_retreat = (lowest_cul_profitrate - highest_in_min) / highest_in_min if highest_in_min != 0 else 0
    sharp_ratio = (profitrate - 1 -norisk_yield*len(pricelist)/(365*12*24)) / (sigma*sqrt((365*12*24))) if sigma > 0 else 0
    calmar_ratio = (profitrate - 1 -norisk_yield*len(pricelist)/(365*5*24)) / abs(max_retreat) if max_retreat < 0 else 0
    CAPM_resultr = OLS(each_tragy_diffratio, add_constant(array(each_long_diffratio).T)).fit()
    max_order_loss=min(each_order_yield)
    G_calmar_ratio=(profitrate - 1 - norisk_yield*len(pricelist)/(365*5*24)) / abs(max_order_loss) if max_order_loss<0 else 1e+234
    alpha = CAPM_resultr.params[0]*365*24*12/(CAPM_resultr.params[0]/CAPM_resultr.tvalues[0])
    beta = CAPM_resultr.params[1]/(CAPM_resultr.params[1]/CAPM_resultr.tvalues[1])

    
    return -(2.5559653367102384 * profitrate -
             30391.887967016268 * sigma +
             1.7226895022326197e-06 * (max_order_loss+max_retreat) +
             2285.6531545522867 * calmar_ratio +
             0.0013132050693759382 * sharp_ratio +
             10898507.741068777 * alpha +
             0.0037153588718620203 * times
             - ((beta) * 38.496196762272554) ** 2)

def opt_signals(beta_vector,factor_matrix):
    signallist = []
    param_k = 2
    closest_3 = lambda x: int(([abs(x+1),abs(x-1)].index(min([abs(x+1),abs(x-1)]))-0.5)*2)  #
    # closest=lambda x:[abs(x-beta_vector[0]),abs(x-beta_vector[1]),abs(x-beta_vector[2])].index(min([abs(x-beta_vector[0]),abs(x-beta_vector[1]),abs(x-beta_vector[2])]))-1
    tanh = lambda x: 1 if x>0 else -1
    sigmoid = lambda x: 1 if x > 0 else 0
    for j in range(len(factor_matrix)):
        xi = array(factor_matrix[j]).dot(beta_vector[:(len(beta_vector) - param_k) / 2])
        alpha = array(factor_matrix[j]).dot(beta_vector[(len(beta_vector) - param_k) / 2:(len(beta_vector) - param_k)])
        for k in range(0, param_k):
            alpha += beta_vector[len(beta_vector) - param_k - 1 + k] * sigmoid(xi)
        signallist.append(float(sigmoid(xi)) * tanh(alpha))

    return signallist
def cal_accuracy(pricelist,signallist):
    trade_cost=0.001
    total =float(0)
    accuracy=float(0)
    cost_price = None
    trend = None
    if len(signallist) == len(pricelist):
        i = 0
        while i < len(signallist) - 2:
            if signallist[i] != 0:
                trend = signallist[i]
                cost_price = pricelist[i]
                #print("open order at ", i, "price at ", cost_price, "trend at", trend)
                if i + 1 < len(signallist):
                    while signallist[i + 1] != 0 and signallist[i+1]==trend:
                        if i + 1 < len(signallist) - 1:
                            i += 1
                        else:
                            break
                    else:
                        i += 1
                        accuracy+= 1 if ( trend * (pricelist[i] - cost_price) / cost_price - trade_cost)>=0 else 0
                        total+=1
                        trend = None
                        cost_price = None
                        #print("close order", i)
                else:
                    break
            else:
                i += 1
    elif len(signallist) < len(pricelist):
        signallist.insert(0, 0)
        i = 0
        while i < len(signallist) - 2:
            if signallist[i] != 0:
                trend = signallist[i]
                cost_price = pricelist[i]
                #print("open order at ", i, "price at ", cost_price, "trend at", trend)
                if i + 1 < len(signallist):
                    while signallist[i + 1] != 0 and signallist[i+1]==trend:
                        if i + 1 < len(signallist) - 1:
                            i += 1
                        else:
                            break
                    else:
                        i += 1
                        accuracy += 1 if (trend * (pricelist[i] - cost_price) / cost_price - trade_cost) >= 0 else 0
                        total += 1
                        trend = None
                        cost_price = None
                        #print("close order", i)
                else:
                    break
            else:
                i += 1
    else:
        pass
    if total==0:
        if cost_price!=None:
            total+=1
            accuracy+=1 if (trend * (pricelist[len(pricelist)-1] - cost_price) / cost_price - trade_cost)>=0 else 0
            return_value=float(accuracy/total)
        else:
            return_value=0
    else:
        return_value = float(accuracy / total)

    print("accuracy",accuracy,'total',total)
    return return_value
def Kline_image(high,low,open,close):
    Image=lambda High_price,Low_price,Open_price,Close_price:(Close_price-Open_price)/(High_price-Low_price) if (High_price-Low_price) !=0 else float(1)
    return_list=list(map(Image,high,low,open,close))
    return return_list
def Average_expyield(price,Param_T):
    Time_list=[i+1 for i in range(Param_T)]
    x=add_constant(array(Time_list).T)
    Get_expyield=lambda data: inv(x.T.dot(x)).dot(x.T).dot(numpy_log(data))[1]
    return [Get_expyield(price[i-Param_T:i]) for i in range(Param_T,len(price))]
def Yield_gap(price,Param_T):
    def cal_Yield_list(input_price):
        lag_price=input_price[1:]
        Yield_list=(array(input_price[:len(input_price)-1])-array(lag_price))/array(input_price[:len(input_price)-1])
        return max(Yield_list)-min(Yield_list)
    return [cal_Yield_list(price[i-Param_T:i]) for i in range(Param_T,len(price))]
def weighted_continuous_signals(close,gap_interval=10,total_num=30):
    SAVE_CONTNUOUSsignals=array([0 for i in close])
    for index_interval in range(gap_interval,gap_interval+total_num*gap_interval,gap_interval):
        got_list=tag_signal_continuous(close,gap_interval+index_interval*gap_interval,trade_cost=trade_cost*2.2)
        print("Weight:",exp(-((index_interval))/((total_num+1)*gap_interval)))
        got_list=array(got_list)*exp(-((index_interval))/((total_num+1)*gap_interval))
        SAVE_CONTNUOUSsignals=SAVE_CONTNUOUSsignals+got_list
    return list(SAVE_CONTNUOUSsignals)
def TRANFERSGINALS(into_list):
    NEWSIGNALS=[into_list[0]]
    NEW_DO_SIGNALS=[1 if into_list[0]!=0 else 0]
    for i in range(1,len(into_list)-1):
        if into_list[i]!=0 and into_list[i+1]==into_list[i]:
            NEWSIGNALS.append(into_list[i])
            NEW_DO_SIGNALS.append(1)
        elif into_list[i+1]!=into_list[i] and into_list[i+1]==-into_list[i]:
            NEWSIGNALS.append(into_list[i+1]*2)
            NEW_DO_SIGNALS.append(1)
        elif into_list[i+1]!=0 and into_list[i]==0:
            NEWSIGNALS.append(into_list[i+1]*2)
            NEW_DO_SIGNALS.append(0)
        else:
            NEWSIGNALS.append(0)
            NEW_DO_SIGNALS.append(0)
    return [NEWSIGNALS,NEW_DO_SIGNALS]
#def TRANs
def trends(into_list):
    output_list=[]
    for i in range(len(into_list)):
        if into_list[i]>1/3:
            output_list.append(1)
        elif into_list[i]<-1/3:
            output_list.append(-1)
        else:
            output_list.append(0)
    return output_list
class ML_GLM_test:
    def __init__(self,sample_file='sample_5min.csv',param_k=6,param_S=100,param_T=100):
        self.time_list=[]
        self.timestamplist=[]
        self.my_close_list=[]
        self.my_max_list=[]
        self.my_min_list=[]
        self.my_volume_list=[]
        self.my_open_list=[]
        self.param_k=param_k
        self.param_S=param_S
        self.data_to_fit_x = []
        self.data_to_fit_y = []
        self.data_to_test_x=[]
        self.data_to_test_y=[]
        self.my_baodan_list=[]
        self.param_t=param_T
        with open(sample_file,'r') as my_samplefile:
            my_data=list(reader(my_samplefile))
            for i in range(0,len((my_data))):
                if i!=0:
                    self.time_list.append(my_data[i][0])
                    self.timestamplist.append(float(my_data[i][1]))
                    self.my_close_list.append(float(my_data[i][5]))
                    self.my_max_list.append(float(my_data[i][3]))
                    self.my_min_list.append(float(my_data[i][4]))
                    self.my_open_list.append(float(my_data[i][2]))
                    self.my_volume_list.append(float(my_data[i][6]))
    def Weighted_build(self):
        got_weight_continuous_signals=weighted_continuous_signals(self.my_close_list)
        self.W_signals = max_min(got_weight_continuous_signals,max=max(got_weight_continuous_signals),min=min(got_weight_continuous_signals))
        TESTW_signals=list(map(closet_3_single,self.W_signals))
        print(cal_profitrate(self.my_close_list,TESTW_signals,plotornot=True,timeline=self.time_list))
        print(cal_accuracy(self.my_close_list, TESTW_signals))
        print("End seTEST")
    def tag_signal(self):
        mutlti=2.2
        self.continuous_signal=array(tag_signal_continuous(self.my_close_list,self.param_S,trade_cost=trade_cost))
        self.tag_list=[{
                            '-4':0,
                            '-3':0,
                            '-2':0,
                            '-1':0,
                            '0':0,
                            '1':0,
                            '2':0,
                            '3':0,
                            '4':0
                        } for i in range(0,len(self.my_close_list))]
        for i in range(0,len(self.my_close_list)-self.param_S-1,self.param_S):
            temp_list=self.my_close_list[i:i+self.param_S]
            index_max=temp_list.index(max(temp_list))
            index_min=temp_list.index(min(temp_list))
            if (max(temp_list)-min(temp_list))/min(temp_list)>trade_cost*mutlti:
                if index_max<index_min:

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost*mutlti:
                            self.tag_list[i ]['2'] += 1
                            self.tag_list[i+index_max]['-3']+=1
                    else:
                            self.tag_list[i]['0'] += 1
                            self.tag_list[i+index_max]['-2']+=1
                    for j in range(1,index_max):

                        if (max(temp_list)-temp_list[0])/temp_list[0]>trade_cost*mutlti:
                            self.tag_list[i+j]['3'] += 1
                        else:
                            self.tag_list[i+j]['0']+=1

                    for j in range(index_max,index_min):
                        self.tag_list[i+j]['-4'] += 1


                    if (temp_list[self.param_S-1]-temp_list[index_min])/temp_list[index_min]>trade_cost*mutlti:
                        self.tag_list[i + index_min]['4'] += 1
                    else:
                        self.tag_list[i+index_min]['-1']+=1

                    for j in range(index_min+1,self.param_S):
                        if (temp_list[self.param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost*mutlti:

                            self.tag_list[i + j]['3'] += 1
                        else:
                            self.tag_list[i + j]['0'] += 1
                    #
                    if (temp_list[self.param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost*mutlti:

                        self.tag_list[i + self.param_S]['1'] += 1
                    else:
                        self.tag_list[i + self.param_S]['0'] += 1

                else:

                    if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost*mutlti:
                        self.tag_list[i]['-2'] += 1
                        self.tag_list[i + index_min]['3'] += 1

                    else:
                        self.tag_list[i]['0'] += 1
                        self.tag_list[i + index_min]['2'] += 1

                    for j in range(1, index_min):


                        if (max(temp_list) - temp_list[0]) / temp_list[0] > trade_cost*mutlti:
                            self.tag_list[i + j]['-3'] += 1
                        else:
                            self.tag_list[i + j]['0'] += 1
                    #
                    for j in range(index_min+1, index_max):
                            self.tag_list[i + j]['4'] += 1
                    #

                    if (temp_list[self.param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost*mutlti:
                        self.tag_list[i + index_min]['-4'] += 1
                    else:
                        self.tag_list[i + index_min]['1'] += 1
                    #
                    for j in range(index_min + 1, self.param_S):

                        if (temp_list[self.param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost*mutlti:

                            self.tag_list[i + j]['-3'] += 1
                        else:
                            self.tag_list[i + j]['0'] += 1
                    #

                    if (temp_list[self.param_S - 1] - temp_list[index_min]) / temp_list[index_min] > trade_cost*mutlti:
                            self.tag_list[i + self.param_S]['-1'] += 1
                    else:
                            self.tag_list[i + self.param_S]['0'] += 1
            else:
                #
                for j in range(0,self.param_S):
                    self.tag_list[i+j]['0']+=1
        self.tagged_line=[None for i in self.tag_list]
        self.do_or_notdo=[None for i in self.tag_list]
        self.buy_or_sell=[None for i in self.tag_list]
        finalsignal_list=[]
        for reading_tag in range(0,len(self.tag_list)):
            signal=[]


            for k in self.tag_list[reading_tag].keys():
                if self.tag_list[reading_tag][k]!=0:
                    signal.append([int(k),self.tag_list[reading_tag][k]])
            if len(signal)==1:
                final_signal=None
                finalsignal_list.append(signal[0][0] if signal[0][0] not in [-4,4] else 0)
                if signal[0][0]==0:
                    final_signal=0
                elif signal[0][0]>0:
                    final_signal=1
                else:
                    final_signal=-1
                self.tagged_line[reading_tag] = final_signal
                if final_signal in [-4, 4]:
                    self.do_or_notdo[reading_tag] = 0
                else:
                    self.do_or_notdo[reading_tag] = 1 if final_signal != 0 else 0  # #
                if final_signal == 0:
                    self.buy_or_sell[reading_tag] = None
                elif final_signal > 0:
                    self.buy_or_sell[reading_tag] = 1
                else:
                    self.buy_or_sell[reading_tag] = -1
            else:
                total_value=0
                for i in signal:
                    total_value+=i[0]/len(signal)
                final_signal = None
                finalsignal_list.append(round(total_value) if round(total_value) not in [-4,4] else 0)
                '''
                if round(total_value)== 0:
                    final_signal = 0
                elif round(total_value) > 0.:
                    final_signal = 1

                else:
                    final_signal = 0
                '''
                if total_value== 0:
                    final_signal = 0
                elif total_value > 0.5:
                    final_signal = 1
                elif total_value <-0.5:
                    final_signal = -1
                else:
                    final_signal = 0
                self.tagged_line[reading_tag] = final_signal
                if final_signal in [-4, 4]:
                    self.do_or_notdo[reading_tag] = 0
                else:
                    self.do_or_notdo[reading_tag] = 1 if final_signal != 0 else 0  # #
                if final_signal==0:
                    self.buy_or_sell[reading_tag]=None
                elif final_signal>0:
                    self.buy_or_sell[reading_tag]=1
                else:
                    self.buy_or_sell[reading_tag] = -1
        self.fre_signals=[]
        for i in range(0,len(self.my_close_list)-1):
            if  (self.my_close_list[i+1]-self.my_close_list[i])/self.my_close_list[i]>trade_cost*mutlti:
                self.fre_signals.append(1)
            elif -(self.my_close_list[i+1]-self.my_close_list[i])/self.my_close_list[i]>trade_cost*mutlti:
                self.fre_signals.append(-1)
            else:
                self.fre_signals.append(0)
        self.fre_signals.insert(0,0)
        self.fre_donotdo=[1 if i!=0 else 0 for i in self.fre_signals]

        self.anotherbuysellsignal = [0 if self.buy_or_sell[i] == None else self.buy_or_sell[i] for i in
                                range(self.buy_or_sell.__len__())]

        '''
        print(cal_profitrate(self.my_close_list,list(map(closest_3,self.continuous_signal)), timeline=self.timestamplist))
        print(cal_profitrate(self.my_close_list,self.anotherbuysellsignal,timeline=self.timestamplist))
        TRANFERSGINALS_result=TRANFERSGINALS(self.anotherbuysellsignal)
        self.TRANSFORM_list=TRANFERSGINALS_result[0]
        self.TRANSFORM_donotdo=TRANFERSGINALS_result[1]
        input("continue?")
        '''


        print("sdfg")
    def tostr(self,yourlist):
        a=''
        for i in yourlist:
            a+=str(i)
        return a
    def generate_factor(self):
        print("begin_gennerate_factor")
        lag_volume=[self.my_volume_list[i-1] for i in range(1,len(self.my_volume_list))]
        lag_close=[self.my_close_list[i-1] for i in range(1,len(self.my_close_list))]
        prev_close_list = self.my_close_list[1:]
        prev_volume_list = self.my_volume_list[1:]
        self.linepart=[(self.my_close_list[i]-self.my_open_list[i])/(self.my_max_list[i]-self.my_min_list[i]) if (self.my_max_list[i]-self.my_min_list[i]) !=0 else None for i in range(0,len(self.my_close_list))]
        self.elastic=[(prev_close_list[i]-lag_close[i])*lag_volume[i]/((prev_volume_list[i]-lag_volume[i])*prev_close_list[i]) if (prev_volume_list[i]-lag_volume[i])!=0 else None for i in range(0,len(prev_close_list))]

        self.diffratio = [(prev_close_list[i] - lag_close[i])  / (
                    lag_close[i])  for i in range(0, len(prev_close_list))]
        self.expyield=Average_expyield(self.my_close_list,self.param_t)
        self.Yieldgap=Yield_gap(self.my_close_list,self.param_t)
        self.RSI=RSI(array(self.my_close_list),self.param_t)
        for i in range(self.param_t):
            self.RSI [i]= 0
        max_linepart=max(avoid_null(self.linepart))
        min_linepart=min(avoid_null(self.linepart))
        max_diffratio=max(avoid_null(self.diffratio))
        min_diffratio=min(avoid_null(self.diffratio))
        max_elastic=max(avoid_null(self.elastic))
        for l in range(0,len(self.linepart)):
            if self.linepart[l]==None:
                self.linepart[l]=max_linepart if  (self.my_max_list[l]-self.my_min_list[l])>0 else -1*max_linepart
        for l in range(0,len(self.elastic)):
            if self.elastic[l]==None:
                self.elastic[l]=max_elastic if prev_close_list[l]-lag_close[l] >0 else -1*max_elastic
        self.maxmin_linepart=max_min(self.linepart,max=334.0,min=-232.999999999)
        self.maxmin_diffratio=max_min(self.diffratio,max=0.31904109589,min=-0.223011297416)
        self.max_min_rsi=max_min(self.RSI,max=100,min=0)
        self.maxmin_yieldgap=max_min(self.Yieldgap,max=max(self.Yieldgap),min=min(self.Yieldgap))
        self.maxmin_expyield=max_min(self.expyield,max=max(self.expyield),min=min(self.expyield))
        self.maxmin_diffratio.insert(0,0)
    def cut_testset_trainingset(self,test_ratio=0.3):
        testset_for_ML_X = []
        testset_for_ML_Y = []
        fitset_for_ML_X=[]
        fitset_for_ML_Y= []
        testset_numbers=[]
        for i in range(0,int(test_ratio*len(self.buy_or_sell))):
            random_number=randint(self.param_k,len(self.buy_or_sell)-1)
            if random_number not in testset_numbers:
                testset_numbers.append(random_number)
                ML_X_set=[self.maxmin_linepart[random_number],self.maxmin_elastic[random_number]]
                for k in range(0,self.param_k):
                    ML_X_set.append(self.maxmin_linepart[random_number - k])
                    ML_X_set.append(self.maxmin_elastic[random_number - k])
                with open('testset.csv','a',newline='') as myfile:
                    writecsv=writer(myfile)
                    data_to_write=ML_X_set
                    data_to_write.append(self.do_or_notdo[random_number]*self.buy_or_sell[random_number])
                    writecsv.writerow(data_to_write)
                with open('randomnumbers.csv','a',newline='') as mysecondfile:
                    writecsv=writer(mysecondfile)
                    data_to_write=[random_number]
                    writecsv.writerow(data_to_write)
                testset_for_ML_X.append(ML_X_set)
                testset_for_ML_Y.append(self.do_or_notdo[random_number]*self.buy_or_sell[random_number])
        for i in range(self.param_k,len(self.buy_or_sell)):
            if i not in testset_numbers:
                ML_X_set = [
                            self.maxmin_linepart[i], self.maxmin_elastic[i]]
                for k in range(0, self.param_k):
                    ML_X_set.append(self.maxmin_linepart[i - k])
                    ML_X_set.append(self.maxmin_elastic[i - k])
                with open('fitset.csv','a',newline='') as myfile:
                    writecsv=writer(myfile)
                    data_to_write=ML_X_set
                    data_to_write.append(self.do_or_notdo[i]*self.buy_or_sell[i])
                    writecsv.writerow(data_to_write)
                fitset_for_ML_X.append(ML_X_set)
                fitset_for_ML_Y.append(self.do_or_notdo[i]*self.buy_or_sell[i])
        return {
            'fit':[fitset_for_ML_X,fitset_for_ML_Y],
            'test':[testset_for_ML_X,testset_for_ML_Y],
            'random_list':testset_numbers
        }
    def fit_bymethod(self,method,*params):
        #self.data_to_fit=self.cut_testset_trainingset()
        if len(self.data_to_fit_x)==0 or len(self.data_to_fit_y)==0:
            ok_csv = read_csv('fitset.csv', iterator=True)
            try:
                while True:
                    chunk = ok_csv.get_chunk(5000)
                    for i in range(0, len(list(chunk._values))):
                        self.data_to_fit_x.append(list(chunk._values[i][:len(list(chunk._values[i])) - 1]))
                        self.data_to_fit_y.append(int(chunk._values[i][len(list(chunk._values[i])) - 1]))
                    print("added one")
            except StopIteration:
                pass
            except pandas.errors.ParserError:
                pass
            print("load fit data finished.")
        else:
            print('Had loaded fit data.')
        if len(self.data_to_test_x)==0 or len(self.data_to_test_y)==0:
            ok_csv = read_csv('testset.csv', iterator=True)
            try:
                while True:
                    chunk = ok_csv.get_chunk(5000)
                    for i in range(0, len(list(chunk._values))):
                        self.data_to_test_x.append(list(chunk._values[i][:len(list(chunk._values[i])) - 1]))
                        self.data_to_test_y.append(int(chunk._values[i][len(list(chunk._values[i])) - 1]))
                    print("added one")
            except StopIteration:
                pass
            except pandas.errors.ParserError:
                pass
            print("load test data finished.")
        else:
            print('Had loaded test data.')

        total_zero = float(0)
        total_positiveone = float(0)
        for i in self.data_to_fit_y:
            if i == 0:
                total_zero += 1
            elif i == 1:
                total_positiveone += 1
            else:
                pass
        print("unbalanced ratio:", total_zero / len(self.tagged_line), "|||", total_positiveone / len(self.tagged_line))
        if method=='ols':
            reg=linear_model.LinearRegression()
            reg.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method,'superparam',params,'||',reg.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',reg.score(self.data_to_test_x,self.data_to_test_y))
        elif method=='rls':
            try:
                assert params != None
                reg = linear_model.Ridge(alpha=params[0])
                reg.fit(self.data_to_fit_x, self.data_to_fit_y)
                print(method, 'superparam',params,'||', reg.score(self.data_to_fit_x, self.data_to_fit_y), '||scores in testset',
                      reg.score(self.data_to_test_x, self.data_to_test_y))
            except AssertionError:
                print("None superparam")
        elif method=='lasso':
            try:
                assert params != None
                reg = linear_model.Lasso(alpha=params[0])
                reg.fit(self.data_to_fit_x, self.data_to_fit_y)
                print(method,'superparam',params, '||', reg.score(self.data_to_fit_x, self.data_to_fit_y), '||scores in testset',
                      reg.score(self.data_to_test_x, self.data_to_test_y))
            except AssertionError:
                print("None superparam")
        elif method=='logistic':
            #self.data_to_fit_x,self.data_to_fit_y=load_iris(return_X_y=True)
            reg=linear_model.LogisticRegression(random_state=0).fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method,'superparam',params,'||',reg.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',reg.score(self.data_to_test_x,self.data_to_test_y))
            signal_list = []
            for i in self.full_x:
                print("add signal   ", int(reg.predict([i])))
                signal_list.append(int(reg.predict([i])))
            print("profit,",cal_profitrate(self.full_price, signal_list))
            print("accuracy",cal_accuracy(self.full_price,signal_list))
            self.logistic_signal = signal_list
        elif method=='svm':
            reg=svm.SVC(decision_function_shape='ovo',kernel='linear')
            reg.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method,'superparam',params,'||',reg.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',reg.score(self.data_to_test_x,self.data_to_test_y))
            signal_list=[]
            for i in self.full_x:
                print("add signal   ",int(reg.predict([i])))
                signal_list.append(int(reg.predict([i])))
            print("profit,", cal_profitrate(self.my_close_list, signal_list))
            print("accuracy", cal_accuracy(self.my_close_list, signal_list))
            self.svm_signal=signal_list
        elif method=='tree':
            reg=tree.DecisionTreeClassifier()
            reg.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(reg)
            print(method,'superparam',params,'||',reg.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',reg.score(self.data_to_test_x,self.data_to_test_y))
            dot_data=tree.export_graphviz(reg,out_file=None)
            graph=graphviz.Source(dot_data)
            graph.render('iris')
            signal_list = []
            for i in self.full_x:
                print("add signal   ", int(reg.predict([i])))
                signal_list.append(int(reg.predict([i])))
            print("profit,", cal_profitrate(self.my_close_list, signal_list))
            print("accuracy", cal_accuracy(self.my_close_list, signal_list))
            self.svm_signal = signal_list
        elif method=='naivebayes':
            clf=naive_bayes.MultinomialNB()
            clf.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method,'superparam',params,'||',clf.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',clf.score(self.data_to_test_x,self.data_to_test_y))
            signal_list = []
            for i in self.full_x:
                print("add signal   ", int(clf.predict([i])))
                signal_list.append(int(clf.predict([i])))
            print("profit,", cal_profitrate(self.full_price, signal_list))
            print("accuracy", cal_accuracy(self.full_price, signal_list))
            self.logistic_signal = signal_list
        elif method=='knn':
            clf=neighbors.KNeighborsClassifier(n_neighbors=params[0])
            clf.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method,'superparam',params,'||',clf.score(self.data_to_fit_x,self.data_to_fit_y),'||scores in testset',clf.score(self.data_to_test_x,self.data_to_test_y))
            signal_list = []
            for i in self.full_x:
                #print("add signal   ", int(clf.predict([i])))
                signal_list.append(int(clf.predict([i])))
            print("profit,", cal_profitrate(self.full_price, signal_list))
            print("accuracy", cal_accuracy(self.full_price, signal_list))
        elif method=='multilayer-perception':
            clf=neural_network.MLPClassifier(solver='adam',hidden_layer_sizes=(params[0],params[1]),random_state=params[2]if len(params)>2 else None)
            clf.fit(self.data_to_fit_x, self.data_to_fit_y)
            print(method, 'superparam', params, '||', clf.score(self.data_to_fit_x, self.data_to_fit_y),
                  '||scores in testset', clf.score(self.data_to_test_x, self.data_to_test_y))
        elif method=='adaboost':
            clf=ensemble.AdaBoostClassifier(algorithm='SAMME',n_estimators=5,base_estimator=linear_model.LogisticRegression() if params[0]=='logistic' else None,random_state=0)
            clf.fit(self.data_to_fit_x,self.data_to_fit_y)
            print(method, 'superparam', params, '||', clf.score(self.data_to_fit_x, self.data_to_fit_y),
                  '||scores in testset', clf.score(self.data_to_test_x, self.data_to_test_y))
        elif method=='randomforest':
            clf=ensemble.RandomForestClassifier(n_estimators=params[0] if len(params)!=0 else 10)
            clf.fit(self.data_to_fit_x, self.data_to_fit_y)
            print(method, 'superparam', params, '||', clf.score(self.data_to_fit_x, self.data_to_fit_y),
                  '||scores in testset', clf.score(self.data_to_test_x, self.data_to_test_y))
            signal_list = []
            for i in self.full_x:
                print("add signal   ", int(clf.predict([i])))
                signal_list.append(int(clf.predict([i])))
            print("profit,", cal_profitrate(self.full_price, signal_list))
            print("accuracy", cal_accuracy(self.full_price, signal_list))
            self.logistic_signal = signal_list
        elif method=='voting':
            clf1=tree.DecisionTreeClassifier()
            clf2=neighbors.KNeighborsClassifier(n_neighbors=50)
            clf3=svm.SVC()
            clf4=naive_bayes.MultinomialNB()
            clf5=linear_model.LogisticRegression(random_state=0)
            model=[clf1,clf2,clf3,clf4,clf5]
            dict_clf={
                0:'tree',
                1:'knn',
                2:'svm',
                3:'naive bayes',
                4:'logistic'
            }
            had_list=[]
            f_judge=lambda x,z:[x.index(i)+1 for i in z]
            stop=False
            while stop==False:
                now_group=sample(model,3)
                group_index=f_judge(model,now_group)
                group_index.sort()
                a=self.tostr(group_index)
                print(self.tostr(group_index))
                if self.tostr(group_index) in had_list:
                    continue
                else:
                    had_list.append(self.tostr(group_index))
                    print("model group:",dict_clf[model.index(now_group[0])],dict_clf[model.index(now_group[1])],dict_clf[model.index(now_group[2])])
                    clf= ensemble.VotingClassifier(estimators=[(dict_clf[model.index(now_group[0])], now_group[0]), (dict_clf[model.index(now_group[1])], now_group[1]), (dict_clf[model.index(now_group[2])], now_group[2])],
            voting = 'hard')
                    clf.fit(self.data_to_fit_x, self.data_to_fit_y)
                    print(method, 'superparam', params, '||', clf.score(self.data_to_fit_x, self.data_to_fit_y),
                  '||scores in testset', clf.score(self.data_to_test_x, self.data_to_test_y))
                if len(had_list)>=10:
                    stop=True
        elif method=='stack':
            clf1 = tree.DecisionTreeClassifier()
            clf2 = neighbors.KNeighborsClassifier(n_neighbors = 50)
            clf3 = svm.SVC()
            clf1.fit(self.data_to_fit_x,self.data_to_fit_y)
            clf2.fit(self.data_to_fit_x, self.data_to_fit_y)
            clf3.fit(self.data_to_fit_x, self.data_to_fit_y)
            clf=ensemble.StackingClassifer(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)],final_estimstor=linear_model.LogisticRegression())
            clf.fit(self.data_to_fit_x, self.data_to_fit_y)
            print(method, 'superparam', params, '||', clf.score(self.data_to_fit_x, self.data_to_fit_y),
                  '||scores in testset', clf.score(self.data_to_test_x, self.data_to_test_y))
        else:
            raise ValueError("wrong method")
        return None
    def transfer_test(self):
        self.otime_list=[]
        self.otimestamplist=[]
        self.omy_close_list=[]
        self.omy_max_list=[]
        self.omy_min_list=[]
        self.omy_open_list=[]
        self.omy_volume_list=[]
        with open('bitmex_5min.csv','r') as my_samplefile:
            my_data=list(reader(my_samplefile))
            for i in range(0,len((my_data))):
                if i!=0:
                    '''
                    if float(my_data[i][1])<1577808000:
                        continue
                    '''


                    self.otime_list.append(my_data[i][0])
                    self.otimestamplist.append(float(my_data[i][1]))
                    self.omy_close_list.append(float(my_data[i][5]))
                    self.omy_max_list.append(float(my_data[i][3]))
                    self.omy_min_list.append(float(my_data[i][4]))
                    self.omy_open_list.append(float(my_data[i][2]))
                    self.omy_volume_list.append(float(my_data[i][6]))

        lag_volume = [self.omy_volume_list[i - 1] for i in range(1, len(self.omy_volume_list))]
        lag_close = [self.omy_close_list[i - 1] for i in range(1, len(self.omy_close_list))]
        prev_close_list = self.omy_close_list[1:]
        prev_volume_list = self.omy_volume_list[1:]
        self.olinepart = [
            (self.omy_close_list[i] - self.omy_open_list[i]) / (self.omy_max_list[i] - self.omy_min_list[i]) if (
                                                                                                                        self.omy_max_list[
                                                                                                                            i] -
                                                                                                                        self.omy_min_list[
                                                                                                                            i]) != 0 else None
            for i in range(0, len(self.omy_close_list))]
        self.oelastic = [(prev_close_list[i] - lag_close[i]) * lag_volume[i] / (
                    (prev_volume_list[i] - lag_volume[i]) * prev_close_list[i]) if (prev_volume_list[i] - lag_volume[
            i]) != 0 else None for i in range(0, len(prev_close_list))]

        self.odiffratio = [(prev_close_list[i] - lag_close[i]) / (
            lag_close[i]) for i in range(0, len(prev_close_list))]
        for l in range(0, len(self.olinepart)):
            if self.olinepart[l] == None:
                self.olinepart[l] = 200.0000000001819 if (self.omy_max_list[l] - self.omy_min_list[
                    l]) > 0 else -236.000000000216
        self.omaxmin_linepart = test_max_min(self.olinepart,max_val=200.0000000001819,min_val=-236.000000000216)
        self.omaxmin_diffratio = test_max_min(self.odiffratio,max_val=0.2465753424657534,min_val=-0.17376630057758416)
        self.omaxmin_diffratio.insert(0, 0)
        self.full_x=[]
        self.full_price=[]
        for i in range(self.param_k,len(self.omy_close_list)):
            one_x=[]
            for j in range(0,self.param_k+1):
                one_x.append(self.omaxmin_linepart[i - j])
                one_x.append(self.omaxmin_diffratio[i-j])
            self.full_x.append(one_x)
            self.full_price.append(self.omy_close_list[i])
        logisitic_signal=[]
        test_price=[]
        for i in range(self.param_k,len(self.full_x)):
            signal_groups=Logistic_signal(self.full_x[i])
            logisitic_signal.append(signal_groups)
            test_price.append(self.omy_close_list[i])
        for i in logisitic_signal:
            with open("record_signal.csv",'a',newline='') as myfile:
                csvwrtite=writer(myfile)
                csvwrtite.writerow([i,1 if i==0 else 0])
        print("proifit", cal_profitrate(test_price, logisitic_signal,plotornot=True,timeline=self.otime_list), 'accurary', cal_accuracy(test_price, logisitic_signal))
    def LGmodeltest_three(self):
        self.factor_list = []
        self.factor_list_2=[]
        self.factor_list_2_complete=[]
        self.two_buysell=[]
        self.TRANSFORM_list = [self.W_signals[i] for i in range(len(self.W_signals))]
        train_factor_list=[]
        test_factor_list=[]
        train_list = []
        test_list = []
        test_proportion = 0.6
        for index in range(self.param_k+self.param_t, len(self.my_close_list)):
            initial_vector = []
            for lag in range(1,self.param_k):
                #这部分是使用滞后周期计算的，所以要减去param_t
                initial_vector.append(self.max_min_rsi[index-lag-self.param_t])
                initial_vector.append(self.maxmin_yieldgap[index - lag - self.param_t])
                initial_vector.append(self.maxmin_expyield[index - lag - self.param_t])
                # 这部分不用
                initial_vector.append(self.maxmin_linepart[index - lag])
                initial_vector.append(self.maxmin_diffratio[index - lag])
                initial_vector.append(self.fre_signals[index-lag])
                initial_vector.append(self.fre_donotdo[index-lag])
            random_uniform=uniform(0,1)
            if random_uniform<=test_proportion:
                print(index,"to train")
                train_factor_list.append(initial_vector)
                train_list.append(self.TRANSFORM_list[index])
            else:
                print(index, "to test")
                test_factor_list.append(initial_vector)
                test_list.append(self.TRANSFORM_list[index])
            self.factor_list.append(initial_vector)
        param_factor=len(train_factor_list[0])
        print(array(train_factor_list).shape)
        x_train=array(train_factor_list)
        y_train = array(train_list)
        x_test = array(test_factor_list)
        y_test=array(test_list)
        #x_train=array(self.factor_list[:int(len(self.factor_list)*test_proportion)])#.reshape((int(len(self.factor_list)*test_proportion),1,(self.param_k-1)*param_factor))
        #x_test=array(self.factor_list[int(len(self.factor_list)*test_proportion):])#.reshape((len(self.factor_list)-int(len(self.factor_list)*test_proportion),1,(self.param_k-1)*param_factor))
        #y_train = array(self.TRANSFORM_list[self.param_k+self.param_t:int(len(self.factor_list) * test_proportion) + (self.param_k)+self.param_t])#to_categorical(self.TRANSFORM_list[self.param_k+self.param_t:int(len(self.factor_list) * test_proportion) + (self.param_k)+self.param_t], 3)
        #y_test = array(self.TRANSFORM_list[int(len(self.factor_list) * test_proportion) + self.param_k+self.param_t :])#to_categorical(self.TRANSFORM_list[int(len(self.factor_list) * test_proportion) + self.param_k+self.param_t :], 3)
        print("Start")
        print(" I Corr:", corr(self.anotherbuysellsignal, self.W_signals))
        x_input=Input(shape=(array(train_factor_list).shape[1],))
        x = Dense(self.param_k, activation='tanh')(x_input)
        x=Dense(int(self.param_k/3),activation='tanh')(x)
        x=Dense(int(self.param_k/9),activation='tanh')(x)
        predictions=Dense(1,activation='tanh')(x)
        model = Model(inputs=x_input,outputs=predictions)

        '''
        序列模型
        model=Sequential()
        model.add(LSTM(units=81, activation='softplus',return_sequences=True))
        #model.add(LSTM(units=9, activation='tanh'))
        model.add(Dense(27, activation='tanh'))
        #model.add(Dense(int(self.param_k*len(self.factor_list[0])*0.1), activation='sigmoid'))
        model.add(Dense(3,activation='elu'))
        model.compile(loss='logcosh', optimizer=Adam())#SGD(lr=0.05,momentum=0.8,decay=0.5)
        '''
        model.compile(loss='mean_absolute_error', optimizer=Adam())  # SGD(momentum=0.8,decay=0.5,nesterov=False)
        model.summary()

        model.fit(x=x_train,y=y_train,validation_data=(x_test,y_test),batch_size=1800,epochs=50)
        score=model.evaluate(x_test,y_test,batch_size=1800)
        print("evalculate:",score)
        input("continue")
        '''
        model_do = Sequential()
        model_do.add(LSTM(units=5 * 10, activation='sigmoid', input_shape=x_train.shape[1:]))
        model_do.add(Dense(2, activation='sigmoid'))
        model_do.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.001, momentum=0.9))
        model_do.fit(x=x_train, y=ydo_train, batch_size=1500, epochs=50)
        score = model_do.evaluate(x_test, ydo_test, batch_size=1500)
        for i in range(len(model1_train)):
            #print(model1_train[i],"gggg",argmax(model1_train[i]))
            signals.append(argmax(model1_train[i])-1)

        for i in range(len(model1_test)):
            signals.append(argmax(model1_test[i])-1)
        '''
        model1_train = model.predict(array(self.factor_list),batch_size=1800)

        #model1_test = model.predict(x_test,batch_size=1800)

        signals=trends(model1_train)
        '''
        
        for i in range(len(model1_test)):
            signals.append(closest_3(model1_test[i])-1)
        print(cal_profitrate(self.my_close_list[int(len(self.factor_list) * test_proportion) + self.param_k+self.param_t :],signallist=goes_signals[int(len(self.factor_list) * test_proportion) :],timeline=self.time_list[self.param_k:]))
        print(cal_accuracy(self.my_close_list[int(len(self.factor_list) * test_proportion) + self.param_k+self.param_t :], signallist=goes_signals[int(len(self.factor_list) * test_proportion):]))
        '''

        goes_signals=list(signals)

        print(cal_profitrate(
            self.my_close_list[ self.param_k + self.param_t:],
            signallist=goes_signals,
            timeline=self.time_list[self.param_k:]))
        print(cal_accuracy(
            self.my_close_list[self.param_k+self.param_t:],
            signallist=goes_signals))
        input("continue")
        print(cal_profitrate(
            self.my_close_list[self.param_k + self.param_t:],
            signallist=list(map(closest_3,model1_train)),
            timeline=self.time_list[self.param_k:]))
        print(cal_accuracy(
            self.my_close_list[self.param_k + self.param_t:],
            signallist=list(map(closest_3,model1_train))))
        print("Corr:",corr(self.anotherbuysellsignal[self.param_t+self.param_k:],list(map(to_list,model1_train))))
        extra_name="withcost" if trade_cost!=0 else ""
        extra_name+="-con"
        ques=int(input("save or not"))

        if ques==0:
            extra_information=input("Extra name information?")
            model.save(str(int(time()))+extra_name+extra_information+".h5")

    def neuralnetwork_modeltest(self):
        self.factor_list = []
        self.factor_list_2=[]
        self.factor_list_2_complete=[]
        self.two_buysell=[]
        for index in range(self.param_k, len(self.my_close_list)):
            initial_vector = []
            initial_vector_2 = []
            for lag in range(1,self.param_k):

                initial_vector.append(self.maxmin_linepart[index - lag])
                initial_vector.append(self.maxmin_diffratio[index - lag])
                initial_vector.append(self.fre_donotdo[index-lag])
                initial_vector.append(self.fre_signals[index - lag])
                initial_vector_2.append(self.maxmin_linepart[index - lag])
                initial_vector_2.append(self.maxmin_diffratio[index - lag])
                initial_vector_2.append(self.fre_signals[index - lag])
                initial_vector_2.append(self.fre_donotdo[index - lag])
            if self.anotherbuysellsignal[index]==0:
                pass
            else:
                self.two_buysell.append(self.anotherbuysellsignal[index])
                self.factor_list_2.append(initial_vector_2)
            self.factor_list.append(initial_vector)
            self.factor_list_2_complete.append(initial_vector_2)

        print(array(self.factor_list).shape)
        x_train=array(self.factor_list[:int(len(self.factor_list)*0.7)]).reshape((int(len(self.factor_list)*0.7),1,(self.param_k-1)*4))
        x_test=array(self.factor_list[int(len(self.factor_list)*0.7):]).reshape((len(self.factor_list)-int(len(self.factor_list)*0.7),1,(self.param_k-1)*4))

        x_train2_complete=array(self.factor_list_2_complete[:int(len(self.factor_list_2_complete)*0.7)]).reshape((int(len(self.factor_list_2_complete)*0.7),1,(self.param_k-1)*4))
        x_test2_complete = array(self.factor_list_2_complete[int(len(self.factor_list_2_complete) * 0.7):]).reshape(
            (len(self.factor_list_2_complete) - int(len(self.factor_list_2_complete) * 0.7), 1, (self.param_k-1) * 4))
        model = Sequential()
        y_train=to_categorical(self.do_or_notdo[self.param_k:int(len(self.factor_list)*0.7)+(self.param_k)],2)
        y_test=to_categorical(self.do_or_notdo[int(len(self.factor_list)*0.7)+self.param_k:],2)
        model.add(LSTM(units=2*10, activation='tanh',input_shape=x_train.shape[1:]))
        model.add(Dense(2,activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.001, momentum=0.9))
        model.fit(x=x_train,y=y_train,batch_size=1500,epochs=50)
        score=model.evaluate(x_test,y_test,batch_size=240)
        print("evalculate:",score)
        x_train_2 = array(self.factor_list_2[:int(len(self.factor_list_2) * 0.7)]).reshape(
            (int(len(self.factor_list_2) * 0.7), 1, (self.param_k-1) * 4))
        x_test_2 = array(self.factor_list_2[int(len(self.factor_list_2) * 0.7):]).reshape(
            (len(self.factor_list_2) - int(len(self.factor_list_2) * 0.7), 1, (self.param_k-1) * 4))
        model_2 = Sequential()
        y_train_2 = to_categorical(self.two_buysell[self.param_k:int(len(self.factor_list_2) * 0.7) + self.param_k], 2)
        y_test_2 = to_categorical(self.two_buysell[int(len(self.factor_list_2) * 0.7) :], 2)
        model_2.add(LSTM(units=2 * 10, activation='sigmoid', input_shape=x_train_2.shape[1:]))
        model_2.add(Dense(2, activation='sigmoid'))
        model_2.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.001, momentum=0.9))
        model_2.fit(x=x_train_2, y=y_train_2, batch_size=1500, epochs=50)
        score = model.evaluate(x_test_2, y_test_2, batch_size=240)
        print("evalculate:", score)

        model1_train=model.predict(x_train)
        model1_test=model.predict(x_test)
        model2_train = model_2.predict(x_train2_complete)
        model2_test = model_2.predict(x_test2_complete)
        goes_signals=[]
        for i in range(len(model1_train)):
            ks=list( model1_train[i]).index(max(list( model1_train[i])))
            ps=list( model2_train[i]).index(max(list( model2_train[i])))
            if ks==1:
                if ps==0:
                    goes_signals.append(-1)
                else:
                    goes_signals.append(1)
            elif ks==0:
                goes_signals.append(0)
        for i in range(len( model2_test)):
            ks = list(model1_test[i]).index(max(list(model1_test[i])))
            ps = list(model2_test[i]).index(max(list(model2_test[i])))
            if ks == 1:
                if ps == 0:
                    goes_signals.append(-1)
                else:
                    goes_signals.append(1)
            else:
                goes_signals.append(0)
        print(cal_profitrate(self.my_close_list[self.param_k:],signallist=goes_signals,timeline=self.time_list[self.param_k:]))
        print(cal_accuracy(self.my_close_list[self.param_k:], signallist=goes_signals))


    def goto_test(self):
        self.factor_list = []
        for index in range(self.param_k,len(self.my_close_list)):
            initial_vector=[1]
            for lag in range(self.param_k):
                initial_vector.append(self.maxmin_linepart[index-lag])
                initial_vector.append(self.maxmin_diffratio[index - lag])
                if lag>0:
                    initial_vector.append(self.fre_signals[index - lag])
                else:
                    pass
            self.factor_list.append(initial_vector)
        beta_vector = [  7.96248731,   2.38700802, -10.9921702 ,  -1.20715532,
        -4.16923941,   0.87244449,   7.70719497,  -1.00673017,
       -10.99229631,  -1.41111396,  -3.09626332,   1.41108625,
         2.04138377,   0.67839085]
        signal_list=opt_signals(beta_vector,self.factor_list)
        print(cal_profitrate(self.my_close_list[self.param_k:],signal_list,plotornot=True,timeline=self.time_list[self.param_k:]))
        print(cal_accuracy(self.my_close_list[self.param_k:],signal_list))
    def BOLL_Stradegy(self,DEVparam_up,DEVparam_down,Cosparam,Sinparam,param_T,type='price'):
        Upper_openposition_params=DEVparam_up#0.6744897501960817
        Downer_openposition_params = DEVparam_down#0.6744897501960817
        temp_price = self.my_close_list[:-1]
        temp_diffratio = list((array(self.my_close_list[1:]) - array(temp_price)) / array(temp_price))
        temp_diffratio.insert(0,0)
        diffratio = temp_diffratio
        test_list=numpy_log(array(diffratio)+ones(len(diffratio))) if type=='logyield' else array(self.my_close_list)
        BOLL_UPPER,BOLL_MA,BOLL_DOWNER=BBANDS( test_list,timeperiod=param_T,nbdevup=Upper_openposition_params,nbdevdn=Downer_openposition_params
                                              )

        def judge_signal(x, upper, downer, ma):
            if x > ma and upper * Sinparam >= x >= upper * Cosparam:
                return 1
            elif x > upper * Sinparam:
                return -1
            elif x > ma and x <= upper * Cosparam:
                return 0
            elif x < ma and downer * Sinparam <= x <= downer * Cosparam:
                return -1
            elif x < downer * Sinparam:
                return 1
            elif x < ma and x >= downer * Cosparam:
                return 0
            else:
                return 0
        BOLL_signals = list(map(judge_signal, test_list[param_T:], BOLL_UPPER, BOLL_DOWNER, BOLL_MA))

        return cal_profitfunc_noprint(self.my_close_list[param_T:],BOLL_signals)
    def opt_BOLL_Stradegy(self):
        bounds = Bounds([0,0, 1, 0], [inf,inf, inf, 1])
        initial_x0 = [0.5,0.5, 1.2, 0.5]
        K_list = []
        value_list = []
        params_list = []
        for k in range(12,12+24*30*12,12):
            print("-"*20)
            print("Now index:", k)
            min_func = lambda x: self.BOLL_Stradegy(DEVparam_up=x[0], DEVparam_down=x[1],Sinparam=x[2], Cosparam=x[3], param_T=k)
            opt_result = basinhopping(func=min_func, x0=initial_x0,disp=True)
            K_list.append(k)
            print("This min val:", opt_result.fun, "Best param:", opt_result.x, "gap:",
                  opt_result.x - array(initial_x0))
            value_list.append(opt_result.fun)
            params_list.append(opt_result.x)
        print("-" * 100, "OK--Done", "-" * 100)
        min_index = value_list.index(min(value_list))
        print("min index", K_list[min_index], "param", params_list[min_index])
    def iter_reg(self):
        self.no_factor_list=[]
        self.factor_list=[]
        for index in range(self.param_k,len(self.my_close_list)):
            initial_vector = []
            for lag in range(self.param_k):
                initial_vector.append(self.maxmin_linepart[index - lag])
                initial_vector.append(self.maxmin_diffratio[index - lag])
                if lag>0:
                    initial_vector.append(self.fre_signals[index - lag])
                else:
                    pass
            self.no_factor_list.append(initial_vector)

        for index in range(self.param_k,len(self.my_close_list)):
            initial_vector=[1]
            for lag in range(self.param_k):
                initial_vector.append(self.maxmin_linepart[index-lag])
                initial_vector.append(self.maxmin_diffratio[index - lag])
                if lag>0:
                    initial_vector.append(self.fre_signals[index - lag])
                else:
                    pass
            self.factor_list.append(initial_vector)

        OLSmodel=linear_model.LinearRegression()
        result=OLSmodel.fit(self.no_factor_list,self.anotherbuysellsignal[self.param_k:])
        result_another=OLSmodel.fit(self.no_factor_list,self.do_or_notdo[self.param_k:])

        initial_beta = [result_another.intercept_]
        for j in result_another.coef_:
            initial_beta.append(j-2)
        del self.no_factor_list
        initial_beta.append(result.intercept_)
        for j in result.coef_:
            initial_beta.append(j-2)
        for j in range(0, self.param_k):
            for k in range(len(initial_beta)):
                initial_beta[k] = normalvariate(mu=0, sigma=10)
        print("random:",initial_beta)
        funcs=lambda x:opt_calprofitrate(self.my_close_list[self.param_k:int(len(self.my_close_list)*0.2)],x,self.factor_list[:int(len(self.my_close_list)*0.2)])
        result=basinhopping(funcs,initial_beta,disp=True)
        print(result)
    def final_regression(self):
        fitset_for_ML_X = []
        fitset_for_ML_X_do=[]
        iv_fitset=[]
        fitset_for_MLbuysell_X=[]
        fitset_for_ML_Y1 = []
        fitset_for_ML_Y2 = []

        allset_for_X=[]
        allset_for_X_do=[]
        alltest_for_X = []
        alltest_for_X_do = []
        print("start ")
        for i in range(self.param_k+int(self.param_S/2), int(len(self.tagged_line))):
                ML_X_set = [
                            self.maxmin_linepart[i],self.maxmin_diffratio[i]]
                ML_withdonotdo_x= [
                            self.maxmin_linepart[i],self.maxmin_diffratio[i]]
                #iv=iv_gen(self.timestamplist[i],self.param_k)
                #do_iv=[0 if j==0 else 1 for j in iv]

                for k in range(1, self.param_k+1):
                    #iv=logistic_prev.predict([signal_line[i-k]])[0]
                    #iv_do=1 if iv!=0 else 0
                    ML_X_set.append(self.maxmin_linepart[i - k])
                    ML_X_set.append(self.maxmin_diffratio[i-k])
                    #ML_X_set.append(iv_factor(self.timestamplist[i-k],False))
                    ML_X_set.append(self.fre_signals[i-k])
                    ML_withdonotdo_x.append(self.maxmin_linepart[i - k])
                    ML_withdonotdo_x.append(self.maxmin_diffratio[i - k])
                    #ML_withdonotdo_x.append(iv_factor(self.timestamplist[i-k]))
                    ML_withdonotdo_x.append(1 if self.fre_signals[i-k]!=0 else 0)
                #fitset_for_ML_X.append(ML_X_set)
                fitset_for_ML_X_do.append(ML_withdonotdo_x)
                fitset_for_ML_Y1.append(self.do_or_notdo[i])
                if self.buy_or_sell[i]!=None:
                    fitset_for_MLbuysell_X.append(ML_X_set)
                    fitset_for_ML_Y2.append(self.buy_or_sell[i])
        print("开始logistic")
        logistic_1 = linear_model.LogisticRegression(random_state=0).fit(fitset_for_ML_X_do, fitset_for_ML_Y1)
        logistic_2 = linear_model.LogisticRegression(random_state=0).fit(fitset_for_MLbuysell_X, fitset_for_ML_Y2)
        print("do or not do", logistic_1.score(fitset_for_ML_X_do, fitset_for_ML_Y1))
        print("buy or sell", logistic_2.score(fitset_for_MLbuysell_X, fitset_for_ML_Y2))
        for i in range(self.param_k+int(self.param_S/2), len(self.tagged_line)):
                all_ML_X_set = [
                            self.maxmin_linepart[i],self.maxmin_diffratio[i]]
                all_ML_X_set_do=[
                            self.maxmin_linepart[i],self.maxmin_diffratio[i]]
                for k in range(1, self.param_k+1):
                    all_ML_X_set.append(self.maxmin_linepart[i - k])
                    all_ML_X_set.append(self.maxmin_diffratio[i-k])
                    #all_ML_X_set.append(iv_factor(self.timestamplist[i-k],False))
                    all_ML_X_set.append(self.fre_signals[i-k])
                    all_ML_X_set_do.append(self.maxmin_linepart[i - k])
                    all_ML_X_set_do.append(self.maxmin_diffratio[i - k])
                    #all_ML_X_set_do.append(iv_factor(self.timestamplist[i-k]))
                    all_ML_X_set_do.append(1 if self.fre_signals[i-k]!=0 else 0)
                allset_for_X.append(all_ML_X_set)
                allset_for_X_do.append(all_ML_X_set_do)
        now_signal=[]
        prob_donotdo=[]
        prob_buysell=[]
        now_signal_2=[]
        now_signal_3=[]
        now_signal_4=[]
        for i in range(self.param_k+int(self.param_S/2),len(self.tagged_line)):
            a=logistic_1.predict([allset_for_X_do[i-self.param_k-int(self.param_S/2)]])
            try:

                doba=1 if int(logistic_1.predict([allset_for_X_do[i-self.param_k-int(self.param_S/2)]])[0])==0 else 0
            #now_signal.append(logistic_2.predict([alltest_for_X[i-self.param_k]])[0]*int(logistic_1.predict([alltest_for_X_do[i-self.param_k]])[0]))
                now_signal_2.append(logistic_2.predict([allset_for_X[i-self.param_k-int(self.param_S/2)]])[0]*int(logistic_1.predict([allset_for_X_do[i-self.param_k-int(self.param_S/2)]])[0]))

            except:
                print("sdfds")

        print("profit rate",
              cal_profitrate(self.my_close_list[self.param_k+int(self.param_S/2):], now_signal_2, plotornot=True, timeline=self.time_list))
        print("accuracy rate", cal_accuracy(self.my_close_list[self.param_k+int(self.param_S/2):], now_signal_2))
        print("profit rate",cal_profitrate(self.my_close_list[self.param_k:],now_signal,plotornot=True,timeline=self.time_list,judge_model=[prob_donotdo,prob_buysell]))
        print("accuracy rate", cal_accuracy(self.my_close_list[self.param_k:], now_signal))
        print("-----------------------")

        print("-----------------------")
        print("profit rate",
              cal_profitrate(self.my_close_list[self.param_k:], now_signal_3, plotornot=True, timeline=self.time_list,
                             judge_model=[prob_donotdo, prob_buysell]))
        print("accuracy rate", cal_accuracy(self.my_close_list[self.param_k:], now_signal_3))
        print("-----------------------")
        print("profit rate",cal_profitrate(self.my_close_list[self.param_k:],now_signal_4,plotornot=True,timeline=self.time_list,judge_model=[prob_donotdo,prob_buysell]))
        print("accuracy rate", cal_accuracy(self.my_close_list[self.param_k:], now_signal_4))
        print("dgdf")

a=ML_GLM_test(param_k=121,param_S=10,param_T=3*120)
#weight_indicators(a.my_close_list)
#a.Weighted_build()
#a.tag_signal()
#a.generate_factor()
#a.final_regression()
print("dsgfds")
#a.iter_reg()
#a.final_regression()
a.opt_BOLL_Stradegy()
#a.BOLL_Stradegy(2,360)
#a.LGmodeltest_three()




