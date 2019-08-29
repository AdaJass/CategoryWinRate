import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
import numpy as np
import json
import factors 

print('reading data ...')
import database as db
# Date, Open, High, Low, Close, Volume
VIX = pd.read_csv('./data/VIXD1.csv', names=['Date', 'Open', 'High', 'Low', 'Close'])
A50 = pd.read_csv('./data/CHINA5015.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'],dtype={'Open':np.float64, 'Close': np.float64, 'High':np.float64, 'Low':np.float64})
NZD = pd.read_csv('./data/NZDUSD15.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], dtype={'Open':np.float64, 'Close': np.float64, 'High':np.float64, 'Low':np.float64})
TEC = pd.read_csv('./data/USTEC15.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], dtype={'Open':np.float64, 'Close': np.float64, 'High':np.float64, 'Low':np.float64})

td_day1 = td(1)
td_m15 = td(minutes=15)
td_h1 = td(hours=1)
mt4_to_time = lambda x:dt.strptime(x,'%Y.%m.%d-%H:%M')
vix_to_time  = lambda x:dt.strptime(x, '%m/%d/%Y')

VIX['Date']=VIX['Date'].apply(vix_to_time)
A50['Date']=A50['Date'].apply(mt4_to_time)
NZD['Date']=NZD['Date'].apply(mt4_to_time)
TEC['Date']=TEC['Date'].apply(mt4_to_time)

print('read data completed.')

winter_time ={
    'cn':3,
    'us': 16
} 
summer_time = {
    'cn': 4,
    'us': 15
}
time_rule = {
    'winter_time':winter_time,
    'summer_time':summer_time
}

typical_price = lambda x:(x.High+x.Low+x.Close)/3
start_time = mt4_to_time('2017.03.16-00:00')
end_time = mt4_to_time('2018.12.31-00:00')
now = start_time
timerule = 'winter_time'
index = 0
while True:
    if now > end_time:
        break
    a50_now = now + td_h1*3
    tem = A50[A50.Date == now]
    if len(tem) == 0:
        a50_now = a50_now + td_h1
        tem = A50[A50.Date == a50_now]
        timerule = 'summer_time'
    else:
        timerule = 'winter_time'

    a50_start_index = tem.index[0]
    ustec_now = now - td_day1 + td_h1 * time_rule[timerule]['us']
    vix_rows = VIX[VIX.Date == now - td_day1]
    vix = vix_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1)
    vix = vix.values[0]
    vix = factors.vix_index(vix)
    a50_rows = A50[a50_start_index: a50_start_index + 4*6]
    a50 = a50_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1).values()
    a50 = factors.data_trend(a50, 'a50')

    weekday = dt.weekday(now)
    






    
    
    




