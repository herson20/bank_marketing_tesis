# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 20:08:22 2021

@author: Herson Urbina
"""




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
#libreria de graficos
import plotly.graph_objs as graf
from plotly.offline import iplot, init_notebook_mode

import warnings
warnings.filterwarnings('ignore')


import os
os.listdir(".")


df_dp = pd.read_csv("./data/bank-additional-full.csv",sep =  ";")

# columnas
df_dp.columns

df_dp["y",'job'].describe()

#contar valires en python
df_dp['y'].value_counts()

#infor categorica
colss = ["y",'job','education']

df_dp1= df_dp
df_dp1[colss] = df_dp1[colss].astype('category')

df_dp1[colss].describe()

df_dp[df_dp["y"]].count()

df_dp.groupby('y').count()


sns.distplot(df_dp['y'])
plt.show()



#graficos
trace1 = graf.Bar(
                x = df_dp.age,
                y = df_dp.y,
                name = "citations",
                marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                             line=dict(color='rgb(0,0,0)',width=1.5)),
                text = df_dp.education)
                
trace1 = {
  'x': df_dp.age,
  'y': df_dp.y,
  'name': 'age',
  'type': 'bar'
};
trace2 = {
  'x': df_dp.job,
  'y': df_dp.y,
  'name': 'job',
  'type': 'bar'
};
        
        
                
layout = {
  'xaxis': {'title': 'Top 3 universities'},
  'barmode': 'relative',
  'title': 'citations and teaching of top 3 universities in 2014'
};
data = [trace1, trace2];
fig = graf.Figure(data = data, layout = layout)
iplot(fig)
iplot.show()







