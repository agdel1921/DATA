# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:24:38 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import pandas.rpy.common as com
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
path = "D:/NTUC/raw_data/rds_source/transaction.rds"
readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
df.to_csv("abc_trial.csv", index=False, encoding='utf8')

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
