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

print('read data completed!\n')

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
start_time = mt4_to_time('2017.03.15-00:00')
end_time = mt4_to_time('2018.12.31-00:00')
now = start_time
timerule = 'winter_time'
index = 0
last_day_a50 = 0
last_day_tec = 0
last_vix = 0
learns = []
while True:
    if now > end_time:
        break
    a50_now = now + td_h1*3
    tem = A50[A50.Date == a50_now]
    if len(tem) == 0:
        a50_now = a50_now + td_h1        
        tem = A50[A50.Date == a50_now]
        if len(tem) == 0:
            now = now + td_day1
            continue
        timerule = 'summer_time'
    else:
        timerule = 'winter_time'
    
    # print('cal a50')
    a50_start_index = tem.index[0]
    a50_rows = A50[a50_start_index: a50_start_index + 4*6]
    a50 = a50_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1)
    a50 = factors.data_trend(a50, 'a50')
    if not last_day_a50:
        last_day_a50 = a50
        print('no last_day_a50 ',last_day_a50)
        now = now + td_day1
        continue    
    # print('cal vix')
    vix_rows = VIX[VIX.Date == now]
    vix = vix_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1)
    if len(vix) is not 0:        
        vix = vix.values[0]
        vix = factors.vix_index(vix)  
    else:
        print(f'no this day vix data {now}')
        vix = last_vix 

    # print('cal tec')
    ustec_now = now + td_h1 * time_rule[timerule]['us']
    tec_start_index = TEC[TEC.Date == ustec_now]
    if len(tec_start_index) is not 0:
        tec_start_index = tec_start_index.index[0]
        tec_rows = TEC[tec_start_index: tec_start_index + 7*4]
        tec = tec_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1)
        tec = factors.data_trend(tec, 'tec')
    else:
        tec = last_day_tec
    # print('cal nzd')
    nzd_start_index = NZD[NZD.Date == now + td_h1]
    if len(nzd_start_index) is not 0:
        nzd_start_index = nzd_start_index.index[0]
        nzd_rows = NZD[nzd_start_index: nzd_start_index + time_rule[timerule]['cn']]
        nzd = nzd_rows[['Open','High','Low','Close']].apply(typical_price, axis = 1)
        nzd = factors.data_trend(nzd, 'nzd')
    else:
        nzd = {
            'nzd_up': False,
            'nzd_down': False,
            'nzd_vib': True,
            'nzd_strength': 0,
            'nzd_trend': 0
        }

    weekday = {'weekday': dt.weekday(now)}
    if not last_day_tec:
        last_day_a50 = a50        
        last_day_tec = tec
        last_vix = vix
        print('no last day tec ',last_day_tec)
        now = now + td_day1
        continue
    last_day = {}
    for k in last_day_a50:
        last_day['lastday_'+k.split('_')[-1]] = last_day_a50[k]
    learn_row = dict({'Date': now},**nzd, **last_day_tec, **last_day, **last_vix, **weekday, **a50)
    learns.append(learn_row.copy())
    print(f'learn for {len(learns)} rows of data. time now is {dt.strftime(now, "%Y.%m.%d-%H:%M")}')
    last_day_a50 = a50
    last_day_tec = tec
    last_vix = vix
    now = now + td_day1

pd.DataFrame(learns, columns = ['Date','nzd_up', 'nzd_down', 'nzd_vib', 'nzd_strength', 'nzd_trend', 'tec_up', 'tec_down', 'tec_vib', 'tec_strength', 'tec_trend', 'lastday_up', 'lastday_down', 'lastday_vib', 'lastday_strength', 'lastday_trend', 'vix', 'weekday', 'a50_up', 'a50_down', 'a50_vib', 'a50_strength', 'a50_trend']).to_csv('./data/learn.csv')
    






    
    
    




