# p = '15'

# basenames=['./data/USTEC', './data/CHINA50','./data/NZDUSD']

# for basename in basenames:
#     with open(basename+p+'.csv','r') as f:
#         lines = f.readlines()
#     for index,line in enumerate(lines):
#         lines[index] = lines[index][:10] +'-' + lines[index][11:]
#         # print(lines[index])
#         # exit()
#     with open(basename+p+'.csv','w') as f:
#         f.writelines(lines)

#################################################################
dtf = pd.read_csv('./data/399300.csv')
dtf = dtf.iloc[::-1]
dtf = dtf[['Date','Close','High','Low','Open','Volume']]