"""
nzd_up  nzd_down  nzd_vib  nzd_strength nzd_trend ustec_up  ustec_down  ustec_vib  ustec_strength ustec_trend lastday_up  lastday_down  lastday_vib  lastday_strength lastday_trend vix weekday result_up  result_down  result_vib  result_strength result_trend
"""

import pandas as pd

try:
    data = pd.read_csv('/db.csv')
except FileNotFoundError:
    data = pd.DataFrame()
    pass

