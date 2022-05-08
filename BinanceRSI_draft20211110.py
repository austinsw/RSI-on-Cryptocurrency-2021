import requests
from datetime import datetime
import numpy as np
import pandas as pd

s = "1619827200000"
e = "1632960999999"
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
  print(len(x))
  #print(x[-1])
  if len(y) == 1: break
#print(x[-1])

x = np.delete(x, [1,2,3,5,6,7,8,9,10], axis=1)
x = np.delete(x, np.where(x[:, 2] != '0'), axis=0)
x = np.delete(x, [2], axis=1)
print(len(x))
#print(x[-1])

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
  return rsi_series

a = RSI(Close)
print(a)







"""
headers=["Open time",	"Open",	"High",	"Low",	"Close",	"Volume",	"Close time",	"Quote asset volume",	"Number of trades",	"Taker buy base asset volume",	"Taker buy quote asset volume",	"Ignore"]
s = "1619827200000"
e = "1632960999999"
sym = "ETHUSDT"
intv = "1h"
url = "https://api2.binance.com/api/v3/klines?symbol=" + sym + "&interval=" + intv + "&startTime=" + s + "&endTime=" + e
df = pd.read_json(url)
df.columns = headers
df = df.set_index("Open time")
s_e = str(df["Close time"].iloc[-1])
#print(s_e)
while s_e != e:
  s = str(df["Close time"].iloc[-1] + 1)
  url = "https://api2.binance.com/api/v3/klines?symbol=" + sym + "&interval=" + intv + "&startTime=" + s + "&endTime=" + e
  df2 = pd.read_json(url)
  df2.columns = headers
  df2 = df2.set_index("Open time")
  s_e = str(df2["Close time"].iloc[-1])
  df.drop(df.tail(1).index,inplace=True)
  df = df.append(df2)
"""
"""
s = str(df["Close time"].iloc[-1] + 1)
url = "https://api2.binance.com/api/v3/klines?symbol=" + sym + "&interval=" + intv + "&startTime=" + s + "&endTime=" + e
df2 = pd.read_json(url)
df2.columns = headers
df2 = df2.set_index("Open time")
df.drop(df.tail(1).index,inplace=True)
print(df2)
df = df.append(df2)
"""
"""print(df)
#Close = df.Close
#print(Close)

test = df.index[-1]
print(type(test))"""

"""
def RSI(Close, period=14):
  # 整理資料
  Chg = Close - Close.shift(1)
  Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
  Chg_pos = Chg_pos.fillna(0)
  Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
  Chg_neg = Chg_neg.fillna(0)

  # 計算平均漲跌幅度
  up_mean = []
  down_mean = []
  for i in range(period+1, len(Chg_pos)+1):
    up_mean.append(np.mean(Chg_pos.values[i-period:i]))
    down_mean.append(np.mean(Chg_neg.values[i-period:i]))

  # 計算 RSI
  rsi = []
  for i in range(len(up_mean)):
    rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
  rsi_series = pd.Series(index = Close.index[period:], data = rsi)
  return rsi_series

a = RSI(Close)
print(a)
"""