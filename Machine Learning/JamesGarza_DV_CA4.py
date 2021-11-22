# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:24:05 2020
@author: jamesgarza
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#data = pd.read_excel("/Users/jamesgarza1/Dropbox/CCT Courses/Data Visuilization and Communication/JamesGarza_DV_CA4.xlsx",sheet_name="Clean Data") # Mac version
data = pd.read_excel("JamesGarza_DV_CA4.xlsx",sheet_name="Clean Data") #pc version

#chart 1 showing average drinks per continent clusted bar chart
allDrink = data.groupby(['continent']).mean().sort_index(axis=1)
sumDrink = data.groupby(['continent']).sum()
labels = data.continent.unique().tolist()
labels.sort()

pos = list(range(len(labels)))
width = 0.30
fig, ax = plt.subplots(figsize=(10,7))
bar1 = ax.bar(pos, allDrink.beer_servings, width, label='Beer Servings',color="coral")
bar2 = ax.bar([p + width for p in pos], allDrink.wine_servings, width, label = 'Wine Servings',color="cornflowerblue")
bar3 = ax.bar([p - width for p in pos], allDrink.spirit_servings, width, label = 'Spirit Servings',color="cadetblue")
ax.set_ylabel('Average Alcohol Consumption')
ax.set_title('Average Alcohol Consumption per Continent',fontsize=20)
ax.set_xticks(pos)
ax.set_xticklabels(labels,rotation=90)
ax.legend(loc='upper left')
fig.tight_layout()
plt.show()

#Chart 2 showting total alcohol per continent line chart
drinksTotal = sumDrink.sum(axis=1)
plt.plot(drinksTotal.index,drinksTotal,color="darkblue",linewidth=5.0)
plt.xticks(rotation=90)
plt.ylabel("Total Alcohol Units")
plt.title("Total Alcohol by Continent",fontsize=30)
plt.show()

#Chart 3 Showing beer servings in Europe bar chart
europe = data[(data.continent == 'Europe')]
drink1 = europe[(europe.beer_servings >= 75)]
fig, axes = plt.subplots(figsize=(10,7))
z = len(drink1)
plt.bar(drink1.country,drink1["beer_servings"],color=["burlywood","crimson","darkblue"])
plt.xticks(np.arange(0,z),drink1.country,rotation=90)
plt.ylabel("Beer Servings",color="darkgreen",fontsize=20)
plt.xlabel("Countries",fontsize=20)
plt.title("Beer Servings by Country in Europe",color="black",fontsize=35)
plt.tight_layout()
plt.show()

#Chart 4 Showing wine servings in Europe bar chart
drink2 = europe[(europe.wine_servings >= 50)]
z = len(drink2)
fig, axes = plt.subplots(figsize=(10,7))
plt.bar(drink2.country,drink2["wine_servings"],color=["coral","cornflowerblue","cadetblue"])
plt.xticks(np.arange(0,z),drink2.country,rotation=90)
plt.ylabel("Wine Servings",color="darkgreen",fontsize=20)
plt.xlabel("Countries",fontsize=20)
plt.title("Wine Servings by Country in Europe",color="black",fontsize=35)
plt.tight_layout()
plt.show()

#Chart 5 Showing spirit servings in Europe bar chart
drink3 = europe[(europe.spirit_servings >= 50)]
z = len(drink3)
alcohol = "spirit_servings"
fig, axes = plt.subplots(figsize=(10,7))
plt.bar(drink3.country,drink3[alcohol],color=["burlywood","crimson","darkblue"])
plt.xticks(np.arange(0,z),drink3.country,rotation=90)
plt.ylabel("Spirit Servings",color="darkgreen",fontsize=20)
plt.xlabel("Countries",fontsize=20)
plt.title("Spirit Servings by Country in Europe",color="black",fontsize=35)
plt.tight_layout()
plt.show()

#Chart 6 Showing alcohol percentages in Europe pie chart
europe = sumDrink.loc['Europe',:]
plt.axis('equal')
plt.pie(europe,autopct='%1.1f%%',labels = ['Beer Servings', 'Wine Servings','Spirit Servings'],
        colors=["coral","cornflowerblue","cadetblue"],textprops=dict(color="w"))
plt.legend(loc='upper right', bbox_to_anchor=(1.18,0.95),title='Types of Alcohol in Europe')
plt.title("Alcohol Servings in Europe",color= "black",fontsize=25)
plt.show()