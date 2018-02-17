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
DCE = DataFrame(list(set(a3).difference(set(a4))),columns=['XDCE']) #大商所
# access the contracts in ZCE but not in ZCE
ZCE = DataFrame(list(set(a4).difference(set(a3))),columns=['XZCE']) #郑商所
s = pd.concat([aa1,aa3,aa2,aa4],axis=0)
s.dropna()

print 'The # of Contracts in CFFEX：',len(CFFEX),' ，','There are：',list(CFFEX['CCFX'])
print 'The # of Contracts in SHFE：',len(SHFE),' ，','There are：',list(SHFE['XSGE'])
print 'The # of Contracts in DCE：',len(DCE),' ，','There are：',list(DCE['XDCE'])
print 'The # of Contracts in ZCE：',len(ZCE),' ，','There are：',list(ZCE['XZCE'])
print 'Delete the repeated Contracts in CFFEX, the remaining：' ,len(SHFE)+len(DCE)+len(ZCE)

```
