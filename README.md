# RSI-on-Cryptocurrency-2021
A project with emphasis on utilizing RSI strategy on cryptocurrency market (pulling data with Binance API, trading simulation, statistical analysis), made in 2021. Results show that it is very unlikely that you would be able to outperform the market by trading with RSI, or even make a profit.

## BinanceRSI

*BinanceRSI.py* is made to pull data with the use of Biance API. It features a Unix datetime conversion from human datetime and trading simulation with a virtual account balance. Also, Biance API allows a more flexible control over time interval (1h, 1m, etc.). The draft file holds some previous version, trials and samples for RSI function, headers, etc.

BinanceRSI was origianlly created on Replit. **Installed packages**: pandas 1.4.2

## TradingSimulation.ipynb

Originally developed on Google Colab, instead of pulling data from Binance API, this program uses the yfinance package to pull data from Yahoo Finance, but the time interval is limited to daily data. It features changing the subject between HSI and BTC and plotting the RSI series, mean and std of profits, and getting t-test results.

## genRSITable.ipynb

Originally developed on Google Colab, this program aims at removing extra stuff on *TradingSimulation.ipynb* to become shareable to others for generating their own summary table of statistics results. It features changing the parameters, such as the test subject, start date, end date, buy flag, sell flag, RSI period, number of day of return. This allows improving the sample size by marking every occurence of buy flag and sell flag.

![BTC14-day-return_RSI7](https://user-images.githubusercontent.com/42607409/167306774-1a72377c-08c9-4a36-bbc8-48f62bd8164c.PNG)
