import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
import numpy as np
import json
import factors 

print('reading data ...')
# Date, Open, High, Low, Close, Volume
VIX = pd.read_csv('./data/VIXD1.csv', names=['Date', 'Open', 'High', 'Low', 'Close'])
A50 = pd.read_csv('./data/399300.csv')
A50 = A50.iloc[::-1]
A50 = A50[['Date','Open','High','Low','Close','Volume']]
TEC = pd.read_csv('./data/US30.csv')

td_day1 = td(1)
td_m15 = td(minutes=15)
td_h1 = td(hours=1)
normal_to_time = lambda x:dt.strptime(x,'%Y-%m-%d')
vix_to_time  = lambda x:dt.strptime(x, '%m/%d/%Y')

VIX['Date']=VIX['Date'].apply(vix_to_time)
A50['Date']=A50['Date'].apply(normal_to_time)
TEC['Date']=TEC['Date'].apply(normal_to_time)

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
start_time = normal_to_time('2013-01-01')
end_time = normal_to_time('2018-06-01')
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
    a50_now = now
    tem = A50[A50.Date == a50_now]
    if len(tem) == 0:
        now = now + td_day1
        continue
        timerule = 'summer_time'
    else:
        timerule = 'winter_time'
    # print('cal a50\n')
    a50 = list(tem.to_dict('indexs').values())
    # print(a50)
    if not len(a50):
        now = now + td_day1
        print('none of a50.')
        continue
    else:
        a50 = a50[0]
    # print('the a50 is: ',a50)
    a50 = factors.data_trend_d1(a50, 'A300')
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
    ustec_now = now
    tem = TEC[TEC.Date == ustec_now]
    tec = list(tem.to_dict('indexs').values())
    # print(tec)
    if len(tem) is not 0:
        tec = factors.data_trend_d1(tec[0], 'US30')
    else:
        tec = last_day_tec
    # print('cal nzd')
    # print(tec)
    # if now > start_time + td(10):
    #     exit(1)
    weekday = {'weekday': dt.weekday(now)}
    if not last_day_tec:
        last_day_a50 = a50        
        last_day_tec = tec
        last_vix = vix
        print('no last day tec ',last_day_tec)
        now = now + td_day1
        continue
    last_day = {}
    for k in last_day_a50:  #in case that a50 and last_day_a50 with the same key.
        last_day['lastday_'+k.split('_')[-1]] = last_day_a50[k]

    learn_row = dict({'Date': now},**last_day_tec, **last_day, **last_vix, **weekday, **a50)
    learns.append(learn_row.copy())
    print(f'learn for {len(learns)} rows of data {learn_row}. time now is {dt.strftime(now, "%Y-%m-%d")}')
    last_day_a50 = a50
    last_day_tec = tec
    last_vix = vix
    now = now + td_day1

pd.DataFrame(learns, columns = ['Date', 'US30_des', 'lastday_des', 'vix', 'weekday', 'A300_des']).to_csv('./data/learn.csv')
