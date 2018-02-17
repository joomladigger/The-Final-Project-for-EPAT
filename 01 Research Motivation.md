# 1. Research idea and motivation
* The project topic: Statistical Arbitrage: Pair trading in China’s Futures Markets.
Stocks cannot be shorted according to current China’s trading rules. Contrary to a more developed market, arbitrage opportunities are not readily realized which suggests there might be opportunities for those looking and able to take advantage of them. Therefore, I decided to focus on China’s futures market using Statistical Arbitrage and Pair trading techniques

* The strategy idea
The trading strategy implemented in this project is called “Statistical Arbitrage Trading”, also known as “Pairs Trading” which is a contrarian strategy designed to profit from the mean-reverting behavior of a certain pair ratio. The assumption behind this strategy is that the spread from pairs that show properties of co-integration is mean reverting in nature and therefore will provide arbitrage opportunities if the spread deviates significantly from the mean.

* Which data set will be used
Data set will come from China Financial Futures Exchange (CFFEX)、Shanghai Futures Exchange (SHFE)、Dalian Commodity Exchange (DCE) and Zhengzhou Commodity Exchange(ZCE). All the daily data from the above four Exchanges will be accessed through UQER’s API (https://uqer.io/).

The trading strategy will be back-tested for the period between 01/01/2008 and 31/12/2017. This period will be divided into an in-sample back-test, which will run between 01/01/2008 and 31/12/2015, and the remainder, which will be used for the out-of-sample backrest.

China Financial Futures Exchange (CFFEX) is a demutualized exchange dedicated to the trading, clearing and settlement of financial futures, options and other derivatives. On September 8, 2006, with the approval of the State Council and China Securities Regulatory Commission (CSRC), CFFEX was established in Shanghai by Shanghai Futures Exchange, Zhengzhou Commodity Exchange, Dalian Commodity Exchange, Shanghai Stock Exchange and Shenzhen Stock Exchange.

Shanghai Futures Exchange (SHFE) is organized under relevant rules and regulations. A self-regulated entity, it performs functions that are specified in its bylaws and state laws and regulations. The China Securities Regulatory Commission (CSRC) regulates it. At present, futures contracts' underlying commodities, i.e., gold, silver, copper, aluminum, lead, steel rebar, steel wire rod, natural rubber, fuel oil and zinc, are listed for trading.

Dalian Commodity Exchange (DCE) is a futures exchange approved by the State Council and regulated by China Securities Regulatory Commission (CSRC). Over the years, through orderly operation and stable development, DCE has already become world’s largest agricultural futures market as well as the largest futures market for oils, plastics, coal, metallurgical coke, and iron ore. It is also an important futures trading center in China. By the end of 2017, a total of 16 futures contracts and 1 option contract have been listed for trading on DCE, which include No.1 soybean, soybean meal, corn, No.2 Soybean, soybean oil, linear low density polyethylene (LLDPE), RBD palm olein, polyvinyl chloride (PVC), metallurgical coke, coking coal, iron ore, egg, fiberboard, blockboard, polypropylene (PP), corn starch futures and soybean meal option.

Zhengzhou Commodity Exchange (ZCE) is the first pilot futures market approved by the State Council. At present, the listed products on ZCE include : wheat (Strong Gluten Wheat and Common Wheat), Early Long Grain Non-glutinous Rice, Japonica Rice, Cotton, Rapeseed, Rapeseed Oil, Rapeseed Meal, White Sugar, Steam Coal, Methanol, Pure Terephthalic Acid (PTA) and Flat Glass, form a comprehensive range of products covering several crucial areas of the national economy include agriculture, energy, chemical industry and construction materials.

* Motivation of choosing this particular strategy domain
My focuses on China’s future market is out of the following main reasons:

To begin with, due to the not-shorting limitation of China’s stock markets, we only can long stocks, which makes it is impossible to do pair trading with stocks in China. Because when we do pair trading, we always long few stocks and short ones with high correlation.

What is more, there are very few algo trading firms/strategies that are operating in the China’s future exchange. I believe this should provide great opportunities, as there is little competition. Contrary to a more developed market, arbitrage opportunities aren’t readily realized which suggests there might be opportunities for those looking and able to take advantage of them.

Last but not the least, UQER (https://uqer.io/) provides excellent APIs, through which I can access all daily main contract data from four future exchange of China. As we all know, high quality data plays a crucial role in algo trading. The accessibility of data is one of important factors We should consider when we are choosing markets and strategies.
