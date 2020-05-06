# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:15:28 2020

@author: disha
"""

import pandas as pd

df = pd.read_fwf("gps170821g.003.txt", delimeter='\t')

# extract variables of interest
df2 = pd.concat([df.YEAR, df.MONTH, df.DAY, df.HOUR, df.MIN, df.SEC,
                 df.GDLAT, df.GLON, df.TEC], axis=1)

lat_min = 20
lat_max = 50
lon_min = -125
lon_max = -60

# extract data belonging to the U.S. sector only
df3 = df2[(df2['GDLAT'].between(lat_min,lat_max)) & (df2['GLON'].between(lon_min, lon_max))]

df3 = df3.rename(columns={df3.columns[0]: "year", 
                    df3.columns[1]: "month",
                    df3.columns[2]: "day",
                    df3.columns[3]: "hour",
                    df3.columns[4]: "minute",
                    df3.columns[5]: "second",
                    df3.columns[6]: "lat",
                    df3.columns[7]: "lon",
                    df3.columns[8]: "tec"
                    })


df_time =  pd.to_datetime(df3[[df3.columns[0], df3.columns[1], df3.columns[2],
                           df3.columns[3], df3.columns[4], df3.columns[5]]])

df4 = pd.concat([df_time, df3['lat'], df3['lon'], df3['tec']], axis=1)

#df4.to_csv('eclipse_us_sector_tec.csv')
