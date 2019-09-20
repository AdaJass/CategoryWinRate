from datetime import datetime

DATA_NORMAL = {
    'nzd': 0.0009,
    'a50': 150,
    'tec': 80,
    'vix': 10,
    'A50': 50,
    'US30': 200
}

def data_trend_m15(data, sym='nzd'):
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
    direction = 0
    if trend>0 and diff > 0:
        up = True
        direction = 1
    if trend>0 and diff < 0:
        down = True
        direction = -1
    if not up and not down:
        vib=True
        direction = 0
    return {
        sym + '_direction': direction,
        sym + '_strength': strength,
        sym + '_trend': trend
    }

def data_trend_d1(data, sym='A50'):
    """data is an dict present a day bar of open high low close volume 

    return a string descript the perform of the day price movement.
    """
    body = data['Close'] - data['Open']
    tail = data['High'] - data['Low']
    prefix = 'a'
    if abs(body)/tail > 10 and tail > 1.5 * DATA_NORMAL[sym]:
        prefix = 'b'

    trend = 0
    for mul in range(1,4):
        if abs(body) > DATA_NORMAL[sym] * mul * 0.35:
            trend = mul 

    if body < 0:
        trend = -trend       

    des = prefix + str(trend)
    return {sym + '_des': des}
        
        

def vix_index(vix):
    fear = 0
    if vix > DATA_NORMAL['vix'] + 4:
        fear = 1
    if vix > DATA_NORMAL['vix'] + 4*2:
        fear = 2
    if vix > DATA_NORMAL['vix'] + 4*3:
        fear = 3
    return {'vix': fear}


def week_day_of(timestr, fmt = '%y-%m-%d %H:%M:%S'):
    now = datetime.strptime(timestr,fmt)
    return datetime.weekday(now)
    
    



