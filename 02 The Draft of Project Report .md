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


```
