# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:00:41 2020

@author: jamesgarza
"""

import pandas as pd
import numpy as np
import keras
import tensorflow as tf
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import matplotlib.pyplot as plt

# get the dataset
df = pd.read_csv('TSLA.csv')

df['Date'] = pd.to_datetime(df['Date'])
df.set_axis(df['Date'], inplace=True)
df.drop(columns=['Adj Close'], inplace=True)

# Setting the text on the Y-axis
plt.ylabel("TSLA Stock Price")

# Setting the size of our graph
df.Close.plot(figsize=(10,5))

closeData = df['Close'].values
closeData = closeData.reshape((-1,1))

splitPercent = 0.80
split = int(splitPercent*len(closeData))

X_train = closeData[:split]
X_test = closeData[split:]

y_train = closeData[:split]
y_test = closeData[split:]

datesTrain = df['Date'][:split]
datesTest = df['Date'][split:]


lookBack = 3

trainGenerator = TimeseriesGenerator(X_train, y_train, length=lookBack, batch_size=20)     
testGenerator = TimeseriesGenerator(X_test, y_test, length=lookBack, batch_size=1)

model = Sequential()
model.add(LSTM(10, activation='relu',input_shape=(lookBack,1)))

model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mse'])

numEpochs = 40
history = model.fit_generator(trainGenerator, epochs=numEpochs, verbose=1)




#X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],len(X_train)))
#y_train = np.reshape(y_train,(y_train.shape[0],y_train.shape[1]))
#X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1]))
#y_test = np.reshape(y_test,(y_test.shape[0],y_test.shape[1]))

"""
# evaluate the model
_, train_mse = model.evaluate(X_train, y_train, verbose=0)
_, test_mse = model.evaluate(X_test, y_test, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_mse, test_mse))

X_train = scaler.inverse_transform(X_train)
X_test = scaler.inverse_transform(X_test)
closeTrain= scaler.inverse_transform(y_train)
closeTest = scaler.inverse_transform(y_test)
testGenerator = scaler.inverse_transform(testGenerator)

trace1 = go.Scatter(x = datesTrain,y = closeTrain,mode = 'lines',name = 'Data')
trace2 = go.Scatter(x = datesTest,y = prediction,mode = 'lines',name = 'Prediction')
trace3 = go.Scatter(x = datesTest,y = closeTest,mode='lines',name = 'Ground Truth')
layout = go.Layout(title = "Tesla Stock",xaxis = {'title' : "Date"},yaxis = {'title' : "Close"})
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig.show()
"""
prediction = model.predict_generator(testGenerator)
closeTrain = y_train.reshape((-1))
closeTest = y_test.reshape((-1))
prediction = prediction.reshape((-1))

close_data = closeData.reshape((-1))

def predict(numPrediction, model):
    predictionList = closeData[-lookBack:]
    
    for _ in range(numPrediction):
        x = predictionList[-lookBack:]
        x = x.reshape((1, lookBack, 1))
        out = model.predict(x)[0][0]
        predictionList = np.append(predictionList, out)
    predictionList = predictionList[lookBack-1:]
        
    return predictionList
    
def predictDates(numPrediction):
    lastDate = df['Date'].values[-1]
    predictionDates = pd.date_range(lastDate, periods=numPrediction+1).tolist()
    return predictionDates

numPrediction = 29
forecast = predict(numPrediction, model)
forecastDates = predictDates(numPrediction)


