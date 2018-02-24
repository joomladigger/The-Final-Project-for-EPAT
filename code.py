# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 17:26:24 2018

@author: taoxing
"""
# import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
#from CAL.PyCAL import *
import matplotlib as mpl
mpl.style.use('bmh')
#sns.set_style('white')# bmhggplot
import matplotlib.pylab as plt
from datetime import  datetime
from pandas import DataFrame, Series
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as ADF


# set the working directory
import os
os.getcwd() # this is to check the current working directory
os.chdir("D://EPAT//09 Final Project//")

# loading data
data = pd.read_csv('price.csv',index_col='id',parse_dates=False)


# using the API of UQER access data
code = list(set(data['exchangeCD']))  #delete the repeated objects 


df = DataFrame()

for i in code:
	df1 = DataFrame(data[data['exchangeCD']==i]['contractObject'])
	df1.columns = [i]
	df = pd.concat([df,df1],axis=1)


    
a1 = list(df['CCFX'])
a2 = list(df['XSGE'])
a3 = list(df['XDCE'])
a4 = list(df['XZCE'])
# access the contracts in CFFEX but not in SHFE
CFFEX = DataFrame(list(set(a1).difference(set(a2))),columns=['CCFX'])
# access the contracts in SHFE but not in CFFEX
SHFE = DataFrame(list(set(a2).difference(set(a1))),columns=['XSGE']) 
# access the contracts in DCE but not in ZCE
DCE = DataFrame(list(set(a3).difference(set(a4))),columns=['XDCE']) 
# access the contracts in ZCE but not in ZCE
ZCE = DataFrame(list(set(a4).difference(set(a3))),columns=['XZCE']) 
s = pd.concat([CFFEX,SHFE,DCE,ZCE],axis=0)
s.dropna()

print ('The # of Contracts in CFFEX：',len(CFFEX),'There are：',list(CFFEX['CCFX']))
print ('The # of Contracts in SHFE：',len(SHFE),'There are：',list(SHFE['XSGE']))
print ('The # of Contracts in DCE：',len(DCE),'There are：',list(DCE['XDCE']))  
print ('The # of Contracts in ZCE：',len(ZCE),'There are：',list(ZCE['XZCE']))
print ('Delete the repeated Contracts in CFFEX, the remaining：',len(SHFE)+len(DCE)+len(ZCE))


## Find trade pairs
# filer the contract with turnover less than 10000

#data = DataAPI.MktMFutdGet(tradeDate='20171229',mainCon=1,contractMark=u"",contractObject=u"",startDate=u"",endDate=u"",field=[u"contractObject",u"exchangeCD",u"tradeDate",u"closePrice",u"turnoverVol"],pandas="1") 
data1 = data[data.turnoverVol > 10000 ][data.exchangeCD != u'CCFX'] # not include Contracts from CCFEX
print ('Main Contracts with Turnover Volumn more than 10000：' ,len(data),'there are:',list(data['contractObject']))
contract_set = list(set(data1['contractObject']))
# Find trading pairs

"""
Now that stocks have been filtered for their data and daily liquidity, 
every possible stock pair for each industry will be tested for cointegration. 
An ADF test will be performed such that, the alternative hypothesis is that the pair
to be tested is stationary. The null hypothesis will be rejected for p-values < 0.05.
"""
def find_cointegrated_pairs(dataframe, critial_level = 0.05): 
    n = dataframe.shape[1] # the length of dateframe
    pvalue_matrix = np.ones((n, n)) # initialize the matrix of p
    keys = dataframe.keys() # get the column names
    pairs = [] # initilize the list for cointegration
    for i in range(n):
        for j in range(i+1, n): # for j bigger than i
            stock1 = dataframe[keys[i]] # obtain the price of two contract
            stock2 = dataframe[keys[j]]
            result = sm.tsa.stattools.coint(stock1, stock2) # get conintegration
            pvalue = result[1] # get the pvalue
            pvalue_matrix[i, j] = pvalue
            if pvalue < critial_level: # if p-value less than the critical level 
                pairs.append((keys[i], keys[j], pvalue)) # record the contract with that p-value
    return pvalue_matrix, pairs

# Cleanning the data 

data = pd.read_csv('price.csv',index_col='tradeDate',parse_dates=True)

df3 = DataFrame() 
for i in contract_set:
    df4 = DataFrame(data[data['contractObject']==i]['settlePrice'])
    df4.columns = [i]
    df3 = pd.concat([df3,df4],axis=1)
 
badFluidity = ['B','BB','FB','FU','JR','LR','PM','RI','RS','SM','WH','WR','TF', 'IH', 'IC', 'T', 'IF']
for i in badFluidity:
    if i in df3.columns:
        del df3[i]  
 
for i in df3.columns:
    if df3[i].dropna().shape[0] <= 500:
        del df3[i]
       

all = df3.dropna().copy()
all.head()
all.to_csv("all_contracts.csv")

fig = plt.figure(figsize=(10,8))
pvalues, pairs = find_cointegrated_pairs(all,0.025)
sns.heatmap(1-pvalues, xticklabels=df3.columns, yticklabels=df3.columns, cmap='RdYlGn_r', mask = (pvalues == 1))
p = DataFrame(pairs,columns=['S1','S2','Pvalue'])
p_sorted = p.sort_index(by='Pvalue')


fig = plt.figure(figsize=(12,8))
stock_df1 = all['TA']
stock_df2 = all['RB']
stock_df1.plot(color='#F4718B')
stock_df2.plot(color='#407CE2')
plt.xlabel("Time"); plt.ylabel("Price")
plt.show()


def print_func(p,all):
    
    for i in range(p.shape[0]):
        
        s1 = p.iloc[i][0]
        s2 = p.iloc[i][1]
        print (i,s1,s2)
        
        stock_df1 = all[s1]
        stock_df2 = all[s2]
        
        fig = plt.figure(figsize=(12,8))
        stock_df1.plot(color='#F4718B')
        stock_df2.plot(color='#407CE2')
        plt.xlabel("Time"); plt.ylabel("Price")
        plt.legend([s1, s2])
        plt.show()
    

def print_func_scatter(p,all):
    
    for i in range(p.shape[0]):
        
        s1 = p.iloc[i][0]
        s2 = p.iloc[i][1]
        #print (i,s1,s2)
        
        stock_df1 = all[s1]
        stock_df2 = all[s2]    
        fig = plt.figure(figsize=(12,8))
        plt.scatter(stock_df1,stock_df2)
        plt.xlabel(s1); plt.ylabel(s2)
        plt.show()
        
print_func(p_sorted, all)

# scatter
print_func_scatter(p_sorted, all)

p_sorted.to_csv("p_sorted.csv")
