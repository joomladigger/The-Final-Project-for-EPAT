# The Draft of Project Report
### 1. Access the daily main contract data from the four future exchanges.
```python
#####  import the necessary libraries ####
import numpy as np
import pandas as pd
import seaborn as sns
from CAL.PyCAL import *
import matplotlib as mpl
mpl.style.use('bmh')
#sns.set_style('white')# bmhggplot
import matplotlib.pylab as plt
from datetime import  datetime
from pandas import DataFrame, Series
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller as ADF

##### access the daily trading price of main contract use UQER's API  #####
field = ['tradeDate','exchangeCD','contractObject','settlePrice','closePrice'] 
#settlePrice——settle price
# using the API of UQER access data
data = DataAPI.MktMFutdGet(tradeDate=u"",mainCon=u"1",contractMark=u"",contractObject=u"",startDate=u"20080101",endDate=u"20171231",field=field,pandas="1")
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

print 'The # of Contracts in CFFEX：',len(CFFEX),'There are：',list(CFFEX['CCFX'])
print 'The # of Contracts in SHFE：',len(SHFE),'There are：',list(SHFE['XSGE'])
print 'The # of Contracts in DCE：',len(DCE),'There are：',list(DCE['XDCE'])
print 'The # of Contracts in ZCE：',len(ZCE),'There are：',list(ZCE['XZCE'])
print 'Delete the repeated Contracts in CFFEX, the remaining：' ,len(SHFE)+len(DCE)+len(ZCE)

OUT:
The # of Contracts in CFFEX： 5 There are： ['TF', 'IH', 'IC', 'T', 'IF']
The # of Contracts in SHFE： 14 There are： ['NI', 'ZN', 'FU', 'AG', 'RU', 'AL', 'PB', 'BU', 'AU', 'SN', 'RB', 'HC', 'CU', 'WR']
The # of Contracts in DCE： 16 There are： ['A', 'C', 'B', 'CS', 'BB', 'PP', 'I', 'J', 'M', 'L', 'JM', 'FB', 'JD', 'V', 'Y', 'P']
The # of Contracts in ZCE： 18 There are： ['MA', 'OI', 'RS', 'SR', 'CF', 'JR', 'WH', 'AP', 'CY', 'LR', 'PM', 'SM', 'FG', 'RM', 'TC', 'RI', 'SF', 'TA']
Delete the repeated Contracts in CFFEX, the remaining： 48
```
### 2. delete the contract with turnover volumn less than 10000 
```python
data = DataAPI.MktMFutdGet(tradeDate='20171229',mainCon=1,contractMark=u"",contractObject=u"",startDate=u"",endDate=u"",field=[u"contractObject",u"exchangeCD",u"tradeDate",u"closePrice",u"turnoverVol"],pandas="1") 
data = data[data.turnoverVol > 10000 ][data.exchangeCD != u'CCFX'] # not include Contracts from CCFEX
print 'Main Contracts with Turnover Volumn more than 10000：' ,len(data),'there are:',list(data['contractObject'])
data
OUT：
Main Contracts with Turnover Volumn more than 10000： 36 there are: ['A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CS', 'CU', 'FG', 'HC', 'I', 'J', 'JD', 'JM', 'L', 'M', 'MA', 'NI', 'OI', 'P', 'PB', 'PP', 'RB', 'RM', 'RU', 'SF', 'SM', 'SN', 'SR', 'TA', 'V', 'Y', 'TC', 'ZN']

contractObject	exchangeCD	tradeDate	closePrice	turnoverVol
0	A	XDCE	2017-12-29	3626.0	132704
1	AG	XSGE	2017-12-29	3883.0	257368
2	AL	XSGE	2017-12-29	15225.0	342742
3	AP	XZCE	2017-12-29	8088.0	25762
4	AU	XSGE	2017-12-29	277.8	70460
7	BU	XSGE	2017-12-29	2622.0	223302
8	C	XDCE	2017-12-29	1816.0	172514
9	CF	XZCE	2017-12-29	14945.0	157698
10	CS	XDCE	2017-12-29	2123.0	107298
11	CU	XSGE	2017-12-29	55580.0	106148
14	FG	XZCE	2017-12-29	1483.0	261232
16	HC	XSGE	2017-12-29	3846.0	772990
17	I	XDCE	2017-12-29	531.5	3406882
21	J	XDCE	2017-12-29	1979.5	584372
22	JD	XDCE	2017-12-29	3815.0	104930
23	JM	XDCE	2017-12-29	1313.0	541822
25	L	XDCE	2017-12-29	9800.0	302284
27	M	XDCE	2017-12-29	2761.0	997662
28	MA	XZCE	2017-12-29	2853.0	834060
29	NI	XSGE	2017-12-29	96870.0	799816
30	OI	XZCE	2017-12-29	6418.0	108138
31	P	XDCE	2017-12-29	5226.0	235898
32	PB	XSGE	2017-12-29	19170.0	45266
34	PP	XDCE	2017-12-29	9285.0	357500
35	RB	XSGE	2017-12-29	3794.0	4377144
37	RM	XZCE	2017-12-29	2290.0	499556
39	RU	XSGE	2017-12-29	14105.0	388104
40	SF	XZCE	2017-12-29	6510.0	383334
41	SM	XZCE	2017-12-29	7236.0	139486
42	SN	XSGE	2017-12-29	144840.0	15210
43	SR	XZCE	2017-12-29	5937.0	159692
45	TA	XZCE	2017-12-29	5520.0	473548
47	V	XDCE	2017-12-29	6655.0	352994
50	Y	XDCE	2017-12-29	5668.0	284374
51	TC	XZCE	2017-12-29	605.4	249790
52	ZN	XSGE	2017-12-29	25725.0	289952
````
### 3. find potential trading pairs
Now that stocks have been filtered for their data and daily liquidity, every possible stock pair for each industry will be tested for cointegration. An ADF test will be performed such that, the alternative hypothesis is that the pairto be tested is stationary. The null hypothesis will be rejected for p-values < 0.05.

'''python
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
'''
