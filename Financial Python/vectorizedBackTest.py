# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:22:38 2021

@author: james garza
"""

import pandas as pd
import matplotlib
%matplotlib inline
from pylab import mpl, plt
import numpy as np

raw = pd.read_csv('aiif_eikon_eod_data.csv')

data = pd.DataFrame(raw['EUR='])
data.rename(columns={'EUR=': 'Price'}, inplace = True)

data['SMA1'] = data['Price'].rolling(42).mean()
data['SMA2'] = data['Price'].rolling(252).mean()

plt.style.use('seaborn')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'

data.plot(title='EUR/USD | 42 & 252 days SMAs', figsize = (10,6))

data['Position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
data.dropna(inplace = True)

data['Position'].plot(ylim=[-1.1, 1.1], title= 'Market Positioning', figsize=(10,6))