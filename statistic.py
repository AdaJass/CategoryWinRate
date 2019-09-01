import pandas as pd
import numpy as np

dtf = pd.read_csv('./data/learn.csv')
# print(dtf.tec_up)

def patter_query(df, *patterns,**pattern_dict):
    query_str = ''
    for pt in patterns:
        query_str += pt +' & '
    for it in pattern_dict:
        query_str = query_str + str(it) + ' == ' + str(pattern_dict[it]) + ' & '

    query_str = query_str.strip('& ')
    print(query_str)
    return df.query(query_str)

def statistic(df):
    indicators = {
        'vix': [0,1,2,3,4],
        'weekday':[0,1,2,3],
        'nzd_direction':[-1,0,1],
        'tec_direction':[-1,0,1],
        'lastday_direction':[-1,0,1]
    }
    result = {
        'a50_direction':[-1,0,1]
    }

    single_patterns = []
    for it in indicators:
        for i in indicators[it]:
            single_patterns.append(it + '==' + str(i))

    double_patters = []
    for i,t in enumerate(single_patterns):
        for j in range(i+1, len(single_patterns)):
            double_patters.append(t + ' & ' + single_patterns[j])
    print(single_patterns, end='\n')
    print(double_patters)

    re_patter = [' & a50_direction==-1', ' & a50_direction==1', ' & a50_direction==0']

    ups = []
    downs = []
    vibs = []
    labels = []
    for it in (single_patterns + double_patters):        
        x = patter_query(df, it)
        if(len(x)<10):
            continue
        y_down = patter_query(x, it + re_patter[0])
        y_up = patter_query(x, it + re_patter[1])
        y_vib = patter_query(x, it + re_patter[2])

        up = len(x) and len(y_up)/len(x)
        vib = len(x) and len(y_vib)/len(x)
        down = len(x) and len(y_down)/len(x)

        ups.append(up)
        vibs.append(down)
        downs.append(vib)
        labels.append(it+f' has_{len(x)}')
    pd.DataFrame({'labels': labels, 'ups':ups, 'vibs':vibs, 'downs': downs}).to_csv('./data/patterns_statis.csv')
    return ups,downs,vibs, labels

if __name__ == "__main__":  
    import matplotlib.pyplot as plt 
    plt.xticks(rotation=90)
    ups,downs,vibs,labels = statistic(dtf)
    # cause there are too many items, so it need to be sort 
    # to just present the first-n items
    # below implement bubble-sort
    length = len(ups)
    for i in range(length):
        for j in range(i+1, length):
            if ups[i] > ups[j]:
                ups[i], ups[j] = ups[j], ups[i]
                downs[i], downs[j] = downs[j], downs[i]
                labels[i], labels[j] = labels[j], labels[i]
                vibs[i], vibs[j] = vibs[j], vibs[i]
    
    ups = ups[:20] + ups[-20:] 
    downs = downs[:20] + downs[-20:]
    labels = labels[:20] + labels[-20:]
    vibs = vibs[:20] + vibs[-20:]
    x = list(range(len(ups)))
    width = 0.25
    print('ups:\n',x, ups)
    plt.bar(x, ups, width=width, label='up', fc = 'y')
    for i in range(len(x)):
        x[i] = x[i] + width
    print('vibs:\n',x, vibs)
    plt.bar(x, vibs, width=width, label='vib', tick_label = labels, fc = 'r')
    for i in range(len(x)):
        x[i] = x[i] + width
    print('downs:\n',x, downs)
    plt.bar(x, downs, width=width, label='down',fc = 'b')
    plt.savefig('./static.jpg')
    plt.show()


    # x1 = patter_query(dtf, 'vix==0', tec_direction=1)
    # y1 = patter_query(dtf, 'vix==0', tec_direction=1, a50_direction=1)

    # x2 = patter_query(dtf, 'vix==0', tec_direction=1)
    # y2 = patter_query(dtf, 'vix==0', tec_direction=1, a50_direction=1)

    # x3 = patter_query(dtf, 'vix==0', 'weekday==[0,1]', tec_direction=-1)
    # y3 = patter_query(dtf, 'vix==0', 'weekday==[0,1]', tec_direction=-1, a50_direction=1)

    # x4 = patter_query(dtf, 'weekday==[1]', 'vix==[0]', 'lastday_direction<0')
    # y4 = patter_query(dtf, 'weekday==[1]', 'vix==[0]', 'lastday_direction<0', a50_direction=-1)

    # y5 = patter_query(dtf,a50_direction=-1)
    # x5 = dtf

    # x6 = patter_query(dtf, 'vix==0', 'weekday==[0]')
    # y6 = patter_query(dtf, 'vix==0', 'weekday==[0]', a50_direction=1)

    # print(f'win rate of x1 is:{len(y1)/len(x1)}, has {len(x1)} patterns, pattern occur rate is {len(x1)/len(dtf)}')
    # print(f'win rate of x2 is:{len(y2)/len(x2)}, has {len(x2)} patterns, pattern occur rate is {len(x2)/len(dtf)}')
    # print(f'win rate of x3 is:{len(y3)/len(x3)}, has {len(x3)} patterns, pattern occur rate is {len(x3)/len(dtf)}')
    # print(f'win rate of x6 is:{len(y6)/len(x6)}, has {len(x6)} patterns, pattern occur rate is {len(x6)/len(dtf)}')
    # print(f'win rate of x4 is:{len(y4)/len(x4)}, has {len(x4)} patterns, pattern occur rate is {len(x4)/len(dtf)}')
    # print(f'win rate of x5 is:{len(y5)/len(x5)}, has {len(x5)} patterns, pattern occur rate is {len(x5)/len(dtf)}')


    # it turns out that to predict the top and bottom of everyday movement is the road to succeed.