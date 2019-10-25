import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td

normal_to_time = lambda x:dt.strptime(x,'%Y-%m-%d')
vix_to_time  = lambda x:dt.strptime(x, '%m/%d/%Y')
time_to_str = lambda x:dt.strftime(x, '%Y-%m-%d')


dtf = pd.read_csv('./data/learn.csv')
VIX = pd.read_csv('./data/VIXD1.csv', names=['Date', 'Open', 'High', 'Low', 'Close'])
A50 = pd.read_csv('./data/399300.csv')
A50 = A50.iloc[::-1]
A50 = A50[['Date','Close','High','Low','Open','Volume']]
TEC = pd.read_csv('./data/US30.csv')

fit = dtf.query('US30_des=="-0xb0" & lastday_des=="-0xb3"')
print(fit)
# import pdb; pdb.set_trace()
fitlist_date = list(fit.iloc[:].Date.values)
print(fitlist_date)
for i,it in enumerate(fitlist_date):
    fitlist_date[i] = time_to_str(normal_to_time(it) - td(1))
print(fitlist_date)
print(TEC.query('Date in '+str(fitlist_date)))