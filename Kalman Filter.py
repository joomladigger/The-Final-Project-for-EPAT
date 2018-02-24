# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 22:38:34 2018

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

import statsmodels.api as sm
from pykalman import KalmanFilter
from scipy import poly1d

def load_data():
# set the working directory
    import os
    os.getcwd() # this is to check the current working directory
    os.chdir("D://EPAT//09 Final Project//")
    all_contracts = pd.read_csv('all_contracts.csv',index_col='tradeDate',parse_dates=True)
    p_sorted = pd.read_csv('p_sorted.csv',index_col='id',parse_dates=False)
    
    return all_contracts,p_sorted


def KalmanFilterAverage(x):
    # Construct a Kalman filter
    from pykalman import KalmanFilter
    kf = KalmanFilter(transition_matrices = [1],
                      observation_matrices = [1],
                      initial_state_mean = 0,
                      initial_state_covariance = 1,
                      observation_covariance=1,
                      transition_covariance=.01)

    # Use the observed values of the price to get a rolling mean
    state_means, _ = kf.filter(x.values)
    state_means = pd.Series(state_means.flatten(), index=x.index)
    return state_means

#  Kalman filter regression
def KalmanFilterRegression(x,y):

    delta = 1e-3
    trans_cov = delta / (1 - delta) * np.eye(2) # How much random walk wiggles
    obs_mat = np.expand_dims(np.vstack([[x], [np.ones(len(x))]]).T, axis=1)
    
    kf = KalmanFilter(n_dim_obs=1, n_dim_state=2, # y is 1-dimensional, (alpha, beta) is 2-dimensional
                      initial_state_mean=[0,0],
                      initial_state_covariance=np.ones((2, 2)),
                      transition_matrices=np.eye(2),
                      observation_matrices=obs_mat,
                      observation_covariance=2,
                      transition_covariance=trans_cov)
    
    # Use the observations y to get running estimates and errors for the state parameters
    state_means, state_covs = kf.filter(y.values)
    return state_means

def plot_reg(x,y,state_means):

    # plot the result of Kalman Filter Regression
    import matplotlib.pylab as plt
    _, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(x.index, state_means[:,0], label='slope')
    axarr[0].legend()
    axarr[1].plot(x.index, state_means[:,1], label='intercept')
    axarr[1].legend()
    plt.tight_layout()
    plt.show()
    
    return True

def plot(x,y):
    x.plot()
    y.plot()
    return True

def plot_reg_time(x,y,state_means): 
    import matplotlib.pylab as plt
    # Plot data points using colormap
    sc = plt.scatter(x, y, s=30, edgecolor='k', alpha=0.7)
    cb = plt.colorbar(sc)
    cb.ax.set_yticklabels([str(p.date()) for p in x[::len(x)//9].index])
    
    
    #################################################################################
    
    # Plot every fifth line
    step = 5
    xi = np.linspace(x.min()-5, x.max()+5, 2)
    colors_l = np.linspace(0.1, 1, len(state_means[::step]))
    for i, beta in enumerate(state_means[::step]):
        plt.plot(xi, beta[0] * xi + beta[1], alpha=.2, lw=1, c=cm(colors_l[i]))
        
    # Plot the OLS regression line
    plt.plot(xi, poly1d(np.polyfit(x, y, 1))(xi), '0.4')
    
    # Label axes
    plt.xlabel(s1)
    plt.ylabel(s2)
    plt.show()
    
    return True

def cal_noise_ratio(x,y,state_means):
    y_hat = x*state_means[:,0] + state_means[:,1]
    R_error = y_hat - y
    R = R_error.std() ** 2
    
    Beta = pd.DataFrame(state_means[:,0])
    Beta_1 = Beta.shift(1)
    Q_error = Beta - Beta_1 
    Q = Q_error.dropna().std() ** 2
    
    # noise ratio, Q/R, which expresses the ratio of the variance of the beta process to that of the price process
    noise_r = Q / R
    return noise_r.iloc[0],R_error.mean(),Q_error.mean()


###############################################################
####### TESTING################################################

all_contracts, p_sorted = load_data()    


#  plot scatter 
s1 = p_sorted.iloc[0][0]
s2 = p_sorted.iloc[0][1]

x = all_contracts[s1]
y = all_contracts[s2]
plot(x,y)
    
state_means = KalmanFilterRegression(x,y)
plot_reg(x,y,state_means)
plot_reg_time(x,y,state_means)

noise_r,r_mean,q_mean = cal_noise_ratio(x,y,state_means)
print (noise_r,r_mean,q_mean)


"""The trading strategy will consist of creating a primary sell signal for the pair 
ratio (short the relatively expensive stock and simultaneously buy the relatively 
cheap stock) if the pair is trading between 2 and 2.25 standard deviations above
the mean, at which point, 75% of the available risk capital for that ratio will be 
sold. A secondary sell signal for the pair ratio appears for the remaining 25% of
 risk capital if the pair’s zscore crosses 2.25 standard deviations. An analogous
 primary buy and secondary buy signals are created when the pair is trading below 
 2 and 2.25 standard deviations respectively below the mean. The usefulness of the
 two-step entry signals will be evaluated using the Sharpe ratio of the aggregate 
 results once the backtesting is complete. Each trade’s exit signal will be triggered 
 once the pair’s zscore crosses 0."""

record = pd.DataFrame()
x_mu = KalmanFilterAverage(x)
y_mu = KalmanFilterAverage(y)


record['x'] = x_mu
record['y'] = y_mu


state_means= KalmanFilterRegression(x_mu,y_mu)
plot_reg(x_mu,y_mu,state_means)
record['beta'] = state_means[:, 0]
record['alpha'] = state_means[:, 1]
record['spread'] = record['y'] - record['beta'] * record['x'] - record['alpha']

record['z_score'] = np.zeros(record.shape[0])



# calculate z-score
for i in range(record.shape[0]):
    record['z_score'][i] = (record['spread'][i] - record['spread'][:i].mean()) / \
                           record['spread'][:i].std()
    
initial_cash = 10000000
record['x_price'] = x
record['y_price'] = y
record['x_position'] = np.zeros(record.shape[0])
record['y_position'] = np.zeros(record.shape[0])
record['cash']= np.zeros(record.shape[0])
record['portfolio']= np.zeros(record.shape[0])
record['margin']= np.zeros(record.shape[0])

record.to_csv("record.csv")

leverage = 0.25
hold_percent = 0

position_open = 0
initial_cash = 1000000

for i in np.arange(record.shape[0]):
    if i == 0:
        record['x_position'][i] = 0
        record['y_position'][i] = 0
        record['cash'][i] = initial_cash
        record['portfolio'][i] = initial_cash
        record['margin'][i] = 0
           
    primary_buy = record['z_score'][i] >= 1.0 and record['z_score'][i] < 1.5
    secondary_buy = record['z_score'][i] >= 1.5 
    primary_sell = record['z_score'][i] <= -1.0 and record['z_score'][i] > -1.5
    secondary_sell = record['z_score'][i] <= -1.5
    close_positioin = position_open > 0 and record['z_score'][i] <= 0 \
                    or position_open < 0 and record['z_score'][i] >= 0 
    
########## OPEN POSITION  ##################################################################  
    if i >= 20 and primary_buy and position_open == 0:
        hold_percent = .75
        num = record['cash'][i] * hold_percent / (2 * leverage) / (record['y_price'][i])
        num = np.floor(num)
        print (i,num)
        
        record['y_position'][i] = num
        record['x_position'][i] = - np.floor((record['beta'][i] * record['y_position'][i]))
        
        delta = np.abs((record['y_position'][i] * record['y_price'][i])) * leverage \
              + np.abs((record['x_position'][i] * record['x_price'][i])) * leverage
              
        record['cash'][i] = record['cash'][i-1] - delta      
        record['margin'][i] = delta
        record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                               + record['y_position'][i] * record['y_price'][i] \
                               + record['cash'][i] + record['margin'][i]
        position_open = hold_percent
        
    elif i >= 20 and secondary_buy:
        hold_percent = 1.0
        num = record['cash'][i] * hold_percent  / (2 * leverage) / (record['y_price'][i])
        num = np.floor(num)
        
        record['y_position'][i] = num
        record['x_position'][i] = - np.floor((record['beta'][i] * record['y_position'][i]))
        
        delta = np.abs((record['y_position'][i] * record['y_price'][i])) * leverage \
              + np.abs((record['x_position'][i] * record['x_price'][i])) * leverage
        record['cash'][i] = record['cash'][i-1] - delta      
        record['margin'][i] = delta
        record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                               + record['y_position'][i] * record['y_price'][i] \
                               + record['cash'][i] + record['margin'][i]
        position_open = hold_percent

    elif i >= 20 and primary_sell and position_open == 0:
        hold_percent = -0.75
        num = record['cash'][i] * hold_percent / (2 * leverage) / (record['y_price'][i])
        num = np.floor(num)
        
        record['y_position'][i] = -num
        record['x_position'][i] = np.floor((record['beta'][i] * record['y_position'][i]))
        
        delta = np.abs((record['y_position'][i] * record['y_price'][i])) * leverage \
              + np.abs((record['x_position'][i] * record['x_price'][i])) * leverage
        record['cash'][i] = record['cash'][i-1] - delta      
        record['margin'][i] = delta
        record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                               + record['y_position'][i] * record['y_price'][i] \
                               + record['cash'][i] + record['margin'][i]
        position_open = hold_percent
        
    elif i >= 20 and secondary_sell:
        hold_percent = -1.0
        num = record['cash'][i] * hold_percent / (2 * leverage) / (record['y_price'][i])
        num = np.floor(num)
        
        record['y_position'][i] = -num
        record['x_position'][i] = np.floor((record['beta'][i] * record['y_position'][i]))
        
        delta = np.abs((record['y_position'][i] * record['y_price'][i])) * leverage \
              + np.abs((record['x_position'][i] * record['x_price'][i])) * leverage
        record['cash'][i] = record['cash'][i-1] - delta      
        record['margin'][i] = delta
        record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                               + record['y_position'][i] * record['y_price'][i] \
                               + record['cash'][i] + record['margin'][i]
        position_open = hold_percent
    else:
        record['x_position'][i] = record['x_position'][i-1]
        record['y_position'][i] = record['y_position'][i-1]
        
        delta = record['y_position'][i] * (record['y_price'][i] - record['y_price'][i-1]) \
              + record['x_position'][i] * (record['x_price'][i] - record['x_price'][i-1])
        
        delta = delta / leverage      
        
        record['margin'][i] = record['margin'][i-1] - delta 
        record['cash'][i] = record['cash'][i-1] + delta
        record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                               + record['y_position'][i] * record['y_price'][i] \
                               + record['cash'][i] + record['margin'][i]
        
########## OPEN POSITION  ##################################################################          
        if i >= 20 and close_positioin:
            delta = record['y_position'][i] * (record['y_price'][i] - record['y_price'][i-1]) \
                  + record['x_position'][i] * (record['x_price'][i] - record['x_price'][i-1])
            delta = delta / leverage      
            record['margin'][i] = record['margin'][i-1] - delta 
            record['cash'][i] = record['cash'][i-1] + delta
            
            record['portfolio'][i] = record['x_position'][i] * record['x_price'][i] \
                                   + record['y_position'][i] * record['y_price'][i] \
                                   + record['cash'][i] + record['margin'][i]
                                   
            
            record['cash'][i] = record['cash'][i] + record['margin'][i] \
                              + record['x_position'][i] * record['x_price'][i] \
                              + record['y_position'][i] * record['y_price'][i]
            record['margin'][i] = 0
            record['x_position'][i] = 0
            record['y_position'][i] = 0
            position_open = 0
                
                
                
    
    
    
    


