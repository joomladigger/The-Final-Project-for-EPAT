### Statistical Arbitrage Using the Kalman Filter
#### * PROBLEM: The cointegration relationship are seldom static: they change quite frequently and often break down completely.
We model the relationship between a pair of securities:  
$\beta(t)  = \beta(t-1) + w $  
the unobserved state variable follows a random walk:  
$ Y(t) = \beta(t)X(t) + v$  
where：  

$ w $~ $N(0, Q) $ meaning $w$ is gaussian noise with zero mean and variance $Q$   
$ v $~ $N(0, R) $ meaning $v$ is gaussian noise with zero mean and variance $R$   

What we are interested:
$ \alpha(t) = Y(t) – Y^*(t) = Y(t) –\ beta(t) X(t)$

As usual, we would standardize the alpha using an estimate of the alpha standard deviation, which is $\sqrt{R}$.  (Alternatively, you can estimate the standard deviation of the alpha directly, using a lookback period based on the alpha half-life).

If the standardized alpha is large enough, the model suggests that the price $Y(t)$ is quoted significantly in excess of the true value.  Hence we would short stock $Y$ and buy stock $X$.  (In this context, where $X$ and $Y$ represent raw prices, you would hold an equal and opposite number of shares in $Y$ and $X$.If $X$ and $Y$ represented returns, you would hold equal and opposite market value in each stock).
