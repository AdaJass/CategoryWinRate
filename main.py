import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
print('reading data ...')
import database as db
# Date, Open, High, Low, Close, Volume
VIX = pd.read_csv('./data/VIXD1.csv', names=['Date', 'Open', 'High', 'Low', 'Close'])
A50 = pd.read_csv('./data/CHINA5015.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
NZD = pd.read_csv('./data/NZDUSD15.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
TEC = pd.read_csv('./data/USTEC15.csv', names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

td_day1 = td(1)
td_m15 = td(minutes=15)
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


start_time = mt4_to_time('2017.03.16-03:00')
end_time = mt4_to_time('2018.12.31-00:00')
now = start_time
index = 0
while True:
    if now > end_time:
        break
    A50['Date'] 
    
    




