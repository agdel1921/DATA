# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 09:56:30 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy
#import ggplot2

import matplotlib
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
path = "D:/NTUC/raw_data/rds_source/n "
readRDS = robjects.r['readRDS']

df = readRDS(path)
df = pandas2ri.ri2py(df)
# Writing ot csv f
df.to_csv("cust_trial_new.csv", index=False, encoding='utf8')
#df_t = df.T
# General Information
df.info()
df.shape
df.unique()
df.ndim
df.dtypes
pd.isnull(df).any
df.describe()
df.head(5)
df.cov()
df.corr()