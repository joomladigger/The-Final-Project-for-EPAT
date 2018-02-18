### Statistical Arbitrage Using the Kalman Filter
#### * PROBLEM: The cointegration relationship are seldom static: they change quite frequently and often break down completely.
we model the relationship between a pair of securities:  
$\beta(t)  = \beta(t-1) + w $  
the unobserved state variable follows a random walk:  
$ Y(t) = \beta(t)X(t) + v$  
where：  

w ~ N(0, Q) meaning w is gaussian noise with zero mean and variance Q  
v ~ N(0, R) meaning v is gaussian noise with zero mean and variance R
