import pandas as pd
import numpy as np

# column_names = ['num','Date','nzd_up', 'nzd_down', 'nzd_vib', 'nzd_strength', 'nzd_trend', 'tec_up', 'tec_down', 'tec_vib', 'tec_strength', 'tec_trend', 'lastday_up', 'lastday_down', 'lastday_vib', 'lastday_strength', 'lastday_trend', 'vix', 'weekday', 'a50_up', 'a50_down', 'a50_vib', 'a50_strength', 'a50_trend']
# column_dtype = {
#     'nzd_up': object, 'nzd_down': bool, 'nzd_vib':bool, 'nzd_strength':np.int32, 'nzd_trend':np.int32, 'tec_up':bool, 'tec_down':bool, 'tec_vib':bool, 'tec_strength':np.int32, 'tec_trend':np.int32, 'lastday_up':bool, 'lastday_down':bool, 'lastday_vib':bool, 'lastday_strength':np.int32, 'lastday_trend':np.int32, 'vix':np.float64, 'weekday':np.int32, 'a50_up':bool, 'a50_down':bool, 'a50_vib':bool, 'a50_strength':np.int32, 'a50_trend':np.int32
# }
df = pd.read_csv('./data/learn.csv')
print(df.tec_up)

