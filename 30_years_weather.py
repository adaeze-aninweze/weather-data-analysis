#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:54:53 2022

@author: adaezeaninweze
"""

import pandas as pd
import numpy as np

df = pd.read_excel(r'/Users/adaezeaninweze/Documents/weather_data/30-years-Würzburg.xlsx', 'Sheet1', engine='openpyxl')
df1 = df.copy()
df1['Measuring_Date'] = df1['Measuring Date'].astype(str)
df1['Date_adj'] = df1['Measuring_Date'] 
df1['Date_adj'] = pd.to_datetime(df1['Date_adj'], format = '%Y%m%d%H')
df2 = df1[['Date_adj', 'Temperature']]
df3 = df2.copy()
df3 = df.groupby(pd.to_datetime(df2.Date_adj).dt.date).agg({'Temperature': 'mean'}).reset_index()
df3['date'] = pd.date_range(start = '01/01/1991', end = '31/12/2021')
df3.drop('Date_adj', axis = 1, inplace = True)
df3['year'] = df3['date'].dt.year
df3['day'] = df3['date'].dt.strftime('%m-%d')
leap = df3[df3['day'] == '02-29'].pivot(index='year', columns='day',
    values='Temperature')
result = df3[df3['day'] != '02-29'].pivot(index='year', columns='day',
    values='Temperature')
final = result.mean(axis = 0)
final_leap = leap.mean(axis = 0)
final = final.to_frame()
final = final.rename({0: "Avg_Temp"}, axis = 1)
final_leap = final_leap.to_frame()
final_leap = final_leap.rename({0: "Avg_Temp"}, axis = 1)
yearly_daily_average = pd.concat([final, final_leap], axis = 0)