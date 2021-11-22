# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 00:25:21 2021

@author: jamesgarza
"""

# Use sklearn support vector regression to predicit our data:
import pandas as pd 
import seaborn as sns
import numpy as np 
from matplotlib import style

# ignore warnings 
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
%matplotlib inline
import sklearn.metrics as sm
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

data = pickle.load( open( "c:/Users/irish/Rechin/SP500_TAs_0_1PC_EMAs_df.p", "rb" ) )
data = data.drop(columns = ['StockType'])

stock = 'AAPL'
df = data[data['Symbol'] == stock]

df['MA'] = (df['High'] + df['Low'] + df['Close']) / 3

origDates = df.index

forecast_out = 5
df['prediction'] = df[['MA']].shift(-forecast_out)
target = df['prediction']
#target['prediction'] = target[['MA']].shift(-forecast_out)
df = df.drop(['Symbol','MA','prediction','2 period EMA','5 period EMA'],axis = 1)
df = df.reset_index(drop=True)

X = np.array(df).reshape(-1,1)
X = X[:-forecast_out]
y = np.array(target)
y = y[:-forecast_out]

split = int(round(len(df) * 0.7,0))
X_train = X[:split,:]
X_test = X[split:,:]

y_train = y[:split]
y_test = y[split:]

reg = RandomForestRegressor(criterion = 'mse',n_estimators = 2000, max_depth =750, min_samples_leaf=10,
                            max_features = 'log2', random_state = 0, bootstrap = True)


reg.fit(X_train, y_train)
















