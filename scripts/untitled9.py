# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:08:42 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import os
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

# set the working directory
path = "D:/NTUC/raw_data/rds_source/"
os.chdir(path)
fls1=os.listdir(path)

# Activating python r object
pandas2ri.activate()
 # read in the rds file and store it in a DF (data frame)
|


        csvPd = pd.read_csv(a2, header=0)
        dest1 = path+a2[:-4]+".xlsx"
        print dest1







readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
df.info()
df.shape
df.ndim
df.dtypes
pd.isnull(df).any
df.describe()
df.head(5)
df.cov()
df.corr()
df.to_csv("abc_trial.csv", index=False, encoding='utf8')
df.plot(kind = 'scatter', x = 'MembersCount', y = 'totalkids')
df['TodCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['YoungCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TeenCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['GradCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TodCount'].sum()
df['TeenCount'].sum()
