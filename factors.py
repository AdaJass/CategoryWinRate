"""Will only deal with period of M15 data
"""
from datetime import datetime

DATA_NORMAL = {
    'nzd': 0.0009,
    'a50': 200,
    'tec': 100,
    'vix': 10
}

def data_trend(data, sym='nzd'):
    """data is an array of typical price
    """
    data = list(data)
    open_ = data[0]
    low = min(data)
    top = max(data)
    up = 0
    down = 0
    for it in data:
        if it >= open_:
            up = up + it - open_
        if it <= open_:
            down = down + open_ - it 
    
    diff = up - down
    diff = diff/len(data)
    trend = 0
    strength = 0
    for mul in range(1,6):
        if abs(diff) > DATA_NORMAL[sym] * mul * 0.2:
            trend = mul
        if top - low > DATA_NORMAL[sym] * mul * 0.5:
            strength = mul
    up=False
    down=False
    vib =False
    if trend>0 and diff > 0:
        up = True
    if trend>0 and diff < 0:
        down = True
    if not up and not down:
        vib=True
    return {
        sym + '_up': up,
        sym + '_down': down,
        sym + '_vib': vib,
        sym + '_strength': strength,
        sym + '_trend': trend
    }

def vix_index(vix):
    fear = 0
    if vix > DATA_NORMAL['vix'] + 6:
        fear = 1
    if vix > DATA_NORMAL['vix'] + 6*2:
        fear = 2
    if vix > DATA_NORMAL['vix'] + 6*3:
        fear = 3
    return {'vix': fear}


def week_day_of(timestr, fmt = '%y-%m-%d %H:%M:%S'):
    now = datetime.strptime(timestr,fmt)
    return datetime.weekday(now)
    
    



