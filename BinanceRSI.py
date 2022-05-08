import requests
from datetime import datetime
import numpy as np
import pandas as pd

def getUnix(y,m,d,h,mi):
  date_time = datetime(y, m, d, h, mi)
  unix_timestamp = datetime.timestamp(date_time)*1000
  return str(int(unix_timestamp))

s = getUnix(2021,5,1,0,0) #"1619827200000"
e = getUnix(2021,9,30,23,59) #"1633046340000"
sym = "ETHUSDT"
intv = "1h"
url = "https://api2.binance.com/api/v3/klines?symbol=" + sym + "&interval=" + intv + "&startTime=" + s + "&endTime=" + e

response = requests.get(url)
x = np.array(response.json()) #numpy_2d_arrays

while x[-1,6] != e:
  url = "https://api2.binance.com/api/v3/klines?symbol=" + sym + "&interval=" + intv + "&startTime=" + x[-1,0] + "&endTime=" + e
  response = requests.get(url)
  y = np.array(response.json())
  x = np.delete(x, -1, 0)
  x = np.concatenate((x, y), axis=0)
  if len(y) == 1: break
  print(len(x))

x = np.delete(x, [1,2,3,5,6,7,8,9,10], axis=1)
x = np.delete(x, np.where(x[:, 2] != '0'), axis=0)
x = np.delete(x, [2], axis=1)

for i in range(len(x)):
  timestamp = datetime.fromtimestamp(int(x[i,0])/1000)
  x[i,0] = timestamp.strftime('%Y-%m-%d %H:%M:%S')

df = pd.DataFrame(x, columns=["Open time", "Close"])
df = df.set_index("Open time")
Close = df.Close.astype(float)

def RSI(Close, period=14):
  Chg = Close - Close.shift(1)
  Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
  Chg_pos = Chg_pos.fillna(0)
  Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
  Chg_neg = Chg_neg.fillna(0)

  up_mean = []
  down_mean = []
  for i in range(period+1, len(Chg_pos)+1):
    up_mean.append(np.mean(Chg_pos.values[i-period:i]))
    down_mean.append(np.mean(Chg_neg.values[i-period:i]))

  rsi = []
  for i in range(len(up_mean)):
    rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
  rsi_series = pd.Series(index = Close.index[period:], data = rsi)

  buy_sell = []
  buy = True
  for i in range(len(rsi_series)-1):
    if buy:
      if rsi_series[i] < 30:
        buy_sell.append(rsi_series.index[i+1])
        buy = False
    else:
      if rsi_series[i] > 70:
        buy_sell.append(rsi_series.index[i+1])
        buy = True
  if len(buy_sell) % 2 != 0:
    try: buy_sell.pop()
    except: pass

  return rsi_series, buy_sell

a = RSI(Close)[0]
print(a)

ac = 1000.0
token = 0.0
bs = RSI(Close)[1]
buy = True
for d in bs:
  if buy:
    print(d)
    print(Close[d], "buy")
    token = ac / Close[d]
    #ac = 0.0
    buy = False
  else:
    print(d)
    print(Close[d], "sell")
    new_ac = token * Close[d]
    token = 0.0
    buy = True
    profit = new_ac - ac
    ac = new_ac
    print("Profit:", profit)
print("Final account balance:", ac)
print("Return:", ac - 1000)
