# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 16:17:02 2020

@author: disha
"""
import pandas as pd
import numpy as np

#%% Read TEC data for the U.S. sector on the day of eclipse

path ='C:\Users\disha\Desktop\eclipse-data-sonification\Madrigal Data'
df = pd.read_csv(path + '\eclipse_us_sector_tec.csv')
df = df.drop(columns=[df.columns[0]])
df = df.rename(columns={df.columns[0]: "datetime"})


#%% Find out the minimum TEC value across the U.S. sector at a time interval of 5 minutes

start_time = '2017-08-21 16:02:30'
end_time = '2017-08-21 20:30:30'
frequency = '5min'
timeFormat = '%Y-%m-%d %H:%M:%S'

def minimum_tec_df(Time):
        minimum = (min(df.tec[(df['datetime']==Time)]))
        df2 = (df.loc[(df['datetime']==Time) & (df['tec']==minimum)])
        return df2

min_df = []

for time in pd.date_range(start_time, end_time, freq=frequency).strftime(timeFormat):
    df3 = minimum_tec_df(time)
    min_df.append(df3)
    
min_df = pd.concat(min_df)

min_df = min_df.rename(columns={min_df.columns[3]: "min_tec"})

#min_df.to_csv('eclipse_us_sector_min_tec.csv')


#%% Create a TEC matrix for a 2D grid of 1 deg latitude x 1 deg longitude at a given time

lat_min = 20
lat_max = 50
lon_min = -125
lon_max = -60

x = np.linspace(lon_min, lon_max, (lon_max-lon_min+1))
y = np.linspace(lat_min, lat_max, (lat_max-lat_min+1))

def tec_matrix(Time):
    z = [ [ 0 for i in range(len(x)) ] for j in range(len(y)) ] 
    for j in range(len(y)):
                  z[j] = map(lambda x,y: np.NAN 
                   if (df.tec[(df.lat==y) & (df.lon==x) & (df.datetime==start_time)]).empty 
                   else (df.tec[(df.lat==y) & (df.lon==x) & (df.datetime==start_time)]).values[0] ,
                   x, [y[j]]*len(x) )
      
    return z
                
#%% Find out TEC values at eclipse path coordinates
    
start_time = '2017-08-21 16:02:30'
end_time = '2017-08-21 17:22:30'
frequency = '5min'
timeFormat = '%Y-%m-%d %H:%M:%S'

p=0

df_eclipse_path = pd.read_csv(path + '\eclipse_path_coordinates.csv')
df_eclipse_path = df_eclipse_path.drop(columns=[df_eclipse_path.columns[0]])

i = 0
tec_eclipse_path = []
for time in pd.date_range(start_time, end_time, freq=frequency).strftime(timeFormat):
    Y = round(df_eclipse_path.lat_eclipse_path[i],0)
    X = round(df_eclipse_path.lon_eclipse_path[i],0)
    if (df.tec[(df.lat==Y) & (df.lon==X) & (df.datetime==time)]).empty :
        tec_eclipse_path.append('nan')      
    else: 
        tec_eclipse_path.append((df.tec[(df.lat==Y) & (df.lon==X) & (df.datetime==time)]).values[0])
    i = i+1


df_eclipse_path_tec = pd.DataFrame(tec_eclipse_path, columns=['tec_eclipse_path'])

df_eclipse_path = pd.concat([df_eclipse_path, df_eclipse_path_tec], axis=1)

#df_eclipse_path.to_csv('eclipse_path_tec.csv')

