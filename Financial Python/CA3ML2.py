# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:27:08 2020

@author: jamesgarza
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import ensemble
import numpy as np
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import seaborn as sns

df = pd.read_excel('UnemploymentRateUSA.xlsx')
df.head()
df.info()
df.describe()
sns.pairplot(df)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.Date, y=df['Male Unemployment Rate'], name='Male Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['Female Unemployment Rate'], name='Female Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['White Unemployment Rate'], name='White Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['Hispanic Unemployment Rate'], name='Hispanic Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['African American Unemployment Rate'], name='African American Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['16 - 19 Unemployment Rate'], name='16 - 19 Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['20 - 24 Unemployment Rate'], name='20 - 24 Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['25 - 34 Unemployment Rate'], name='25 - 34 Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['35 - 44 Unemployment Rate'], name='35 - 44 Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['45 - 54 Unemployment Rate'], name='45 - 54 Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['55 and Over Unemployment Rate'], name='55 and Over Unemployment Rate'))
fig.add_trace(go.Scatter(x=df.Date, y=df['Unemployment Rate'], name='Unemployment Rate',line=dict(width=5)))
fig.update_layout(title = {'text' : "USA Unemployment Rate",'x':0.43,'xanchor':'center','y':0.9,'yanchor':'top',
                          'font':{'size':40}}, xaxis_title ='Dates', yaxis_title = 'Price', xaxis_rangeslider_visible=True)
fig.show()

featureData = df[['Male Unemployment Rate','Female Unemployment Rate','White Unemployment Rate','Hispanic Unemployment Rate',
        'African American Unemployment Rate','16 - 19 Unemployment Rate','20 - 24 Unemployment Rate','25 - 34 Unemployment Rate',
        '35 - 44 Unemployment Rate','45 - 54 Unemployment Rate','55 and Over Unemployment Rate']]

X = df.iloc[:,1:12].values
y = df.iloc[:,12].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

params = {'n_estimators': 55, 
          'max_depth': 3, 
          'min_samples_split': 2,
          'learning_rate': 0.05, 
          'loss': 'ls'}
model = ensemble.GradientBoostingRegressor(**params)
model.fit(X_train, y_train)

y_predicted = model.predict(X_test)

print("Accuracy on training set: {:.3f}".format(model.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(model.score(X_test, y_test)))

# The mean squared error
print("Mean squared error: %.2f"% mean_squared_error(y_test, y_predicted))
# Explained variance score: 1 is perfect prediction
print('Test Variance score: %.2f' % r2_score(y_test, y_predicted))

fig, ax = plt.subplots()
ax.scatter(y_test, y_predicted, edgecolors=(0, 0, 0))
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Actual')
ax.set_ylabel('Measured')
ax.set_title("Actual vs Measured")
plt.show()

labels = featureData.columns
importance = model.feature_importances_

features = pd.DataFrame({'label':labels,'score':importance})

features.head(11)

fig = px.bar(features, y='score',x='label',text='score')
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside') #needs to be fixed to percentage not millions
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.show()











