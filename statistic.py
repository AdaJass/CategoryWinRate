import pandas as pd
import numpy as np

dtf = pd.read_csv('./data/learn.csv')
print(dtf)

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
        'weekday':[0,1,2,3,4],
        'US30_des':['"-0xb3"','"-0xb2"','"-0xb1"','"-0xb0"','"-0xa2"','"-0xa1"','"-0xa0"','"0xa0"','"0xa1"','"0xa2"','"0xb0"','"0xb1"','"0xb2"','"0xb3"'],
        'lastday_des':['"-0xb3"','"-0xb2"','"-0xb1"','"-0xb0"','"-0xa2"','"-0xa1"','"-0xa0"','"0xa0"','"0xa1"','"0xa2"','"0xb0"','"0xb1"','"0xb2"','"0xb3"']
    }

    result = {
        'A300_des':['-0xb3','-0xb2','-0xb1','-0xb0','-0xa2','-0xa1','-0xa0','0xa0','0xa1','0xa2','0xb0','0xb1','0xb2','0xb3']
    }

    single_patterns = []
    for it in indicators:
        for i in indicators[it]:
            single_patterns.append(it + '==' + str(i))

    
    double_patters = []
    for i,t in enumerate(single_patterns):
        for j in range(i+1, len(single_patterns)):
            if single_patterns[j][:3] == t[:3]:
                continue
            double_patters.append(t + ' & ' + single_patterns[j])
    
    i,j,k=0,1,2
    thrible = []
    while True:
        if i>=len(single_patterns):
            break
        if i>=j:
            j+=1
            continue
        if j>=k:
            k+=1
            continue        
        # print('~~',i,j,k)
        if j>=len(single_patterns):
            i+=1
            j=0
            k=0
            continue
        if k>=len(single_patterns):            
            j+=1
            k=0
            continue
        
        # print(i,j,k)
        if single_patterns[i][:3] == single_patterns[j][:3]:
            j+=1
            k=0
            continue
        if single_patterns[j][:3] == single_patterns[k][:3]:
            k+=1
            continue
        thrible.append(single_patterns[i] + ' & ' + single_patterns[j] + ' & ' + single_patterns[k])
        k+=1
    print(thrible)
    # exit(1)

    i,j,k,l=0,1,2,3
    penta = []
    while True:
        if i>=len(single_patterns):
            break  
        if i>=j:
            j+=1
            continue
        if j>=k:
            k+=1
            continue
        if k>=l:
            l+=1
            continue         
        
        if j>=len(single_patterns):
            i+=1
            j=0
            k=1
            l=2
            continue
        if k>=len(single_patterns):
            k=0
            l=1
            j+=1
            continue
        if l>=len(single_patterns):
            l=0
            k+=1
            continue
        
            
        if single_patterns[i][:3] == single_patterns[j][:3]:
            j+=1
            k=0
            l=1
            continue
        if single_patterns[j][:3] == single_patterns[k][:3]:
            k+=1
            l=0
            continue
        if single_patterns[k][:3] == single_patterns[l][:3]:
            l+=1
            continue
        penta.append(single_patterns[i] + ' & ' + single_patterns[j] + ' & ' + single_patterns[k] + ' & ' + single_patterns[l])
        k+=1
    print(penta)
    # exit(1)

    # base = [0]
    # def carray(index):
    #     nonlocal base
    #     print(base,'ssss')
    #     if base[index]>=len(single_patterns) or (base[index] >= len(single_patterns)-1 and index < len(base)-1):
    #         if index>0:
    #             if base[index-1] +2 <len(single_patterns):
    #                 base[index-1] = base[index-1] +1
    #                 base[index]=base[index-1]+1
        # if singrle_patterns[k][:3] == single_patterns[l][:3]:
    #             else:
    #                 base[index-1] = base[index-1] +1
    #                 carray(index-1)
    #                 base[index] = base[index-1] + 1 
    #         else:
    #             base = [0]+base  
    #             for i in range(1,len(base)):
    #                 base[i] = base[i-1] +1          

    # all_patterns = []
    # while True: 
    #     if base[-1] >= len(single_patterns):
    #         carray(len(base)-1)
    #     if len(base)>=2:
    #         for ii in range(len(base)): 
    #             if ii<1:
    #                 continue
    #             if single_patterns[base[ii]][:3] == single_patterns[base[ii-1]][:3] or base[ii] <= base[ii-1]:
    #                 base[-1] = base[-1]+1
    #                 break
                
    #     if base[-1] >= len(single_patterns):
    #         carray(len(base)-1)
    #     if base[-1] >= len(single_patterns):
    #         continue
    #     pts = ''
    #     print(base)
    #     for i in base:
    #         pts += single_patterns[i] + ' & '

    #     all_patterns.append(pts.strip('& '))
    #     base[-1]=base[-1]+1
        
    #     if len(base) >= 5:
    #         break
        
    # print(all_patterns[-100:])
    # print(base)
    # exit(1) 

    # re_patter = [' & a50_direction==-1', ' & a50_direction==1', ' & a50_direction==0']

    ups = []
    downs = []
    vibs = []
    labels = []
    for it in (single_patterns + double_patters + thrible + penta):        
        x = patter_query(df, it)
        if(len(x)<6):
            continue
        x = patter_query(df, it)
        # print(x)
        y_down = patter_query(x, it + " & A300_des in ['-0xb3','-0xb2','-0xb1','-0xb0']")
        # print(y_down)
        y_up = patter_query(x, it + " & A300_des in ['0xb0','0xb1','0xb2','0xb3']")
        y_vib = patter_query(x, it + " & A300_des in ['-0xa2','-0xa1','-0xa0','0xa0','0xa1','0xa2']")

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
    plt.xticks(rotation=30)
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