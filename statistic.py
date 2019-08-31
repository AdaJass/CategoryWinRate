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
    pass


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

    up_labels = []
    ups = []
    down_labels = []
    downs = []
    vib_labels = []
    vibs = []
    for it in (single_patterns + double_patters):
        x = patter_query(df, it)

        y_down = patter_query(x, it + re_patter[0])
        y_up = patter_query(x, it + re_patter[1])
        y_vib = patter_query(x, it + re_patter[2])
        
        ups.append(len(y_up)/len(x))
        labels.append(it+'_up')
        vibs.append(len(y_vib)/len(x))
        labels.append(it+'_vib')
        downs.append(len(y_down)/len(x))
        labels.append(it+'_down')
    return up_labels,ups,down_labels,downs,vibs,vib_labels
    pass

if __name__ == "__main__":  
    import matplotlib.pyplot as plt 
    statics, labels = statistic(dtf)
    up
    plt.bar(x, num_list, width=width, label='boy',fc = 'y')
    plt.bar(x, num_list1, width=width, label='girl',tick_label = name_list,fc = 'r')

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