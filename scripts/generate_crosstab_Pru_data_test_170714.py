# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:31:59 2017

@author: Latize
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import os
import time
import copy
import matplotlib.pyplot as plt
import collections


#path = 'D:/training/Prudential/'
#path0 = 'D:/training/Prudential/data/'
#path1 = 'D:/training/Prudential/data/data/'
#path2 = 'D:/training/Prudential/data/vd_test/'
path1 = 'C:/data/data/'
path1 = 'C:/data/test16/'
path2 = 'C:/data/vd_test/test16/'

os.chdir(path1)

dirs = [x[0] for x in os.walk(path1)]
dirs = dirs[1:]
print dirs
       
for path_n in dirs:
    os.chdir(path_n)
    print path_n
    fls = [fl for fl in os.listdir(path_n) if fl[:12]=="custProfile_"]
    if len(fls)>0:
        print fls, len(fls[0])    
        start_amg = time.time()
        amgPd = pd.DataFrame()
        #premiumFileName = 'premium_combo.csv'
        premiumFileName = fls[0]
        
        # read in the Component-level Premium file
        for chunk in pd.read_csv(path_n+"/"+premiumFileName, chunksize = 100000, low_memory=False):
            amgPd = pd.concat([amgPd,chunk])
        end_amg = time.time()
        print amgPd.shape
    
        custNum = list(amgPd.cownnum)
    
        print np.unique(np.array(amgPd.noifp))
    
        amgPd['fullProdName'] = amgPd['cnttype']+' '+amgPd['crtable']
        
        amgPd = amgPd[['cownnum','fullProdName']]
        
        user_u = list(sorted(amgPd.cownnum.unique()))
        item_u = list(sorted(amgPd.fullProdName.unique()))
        
        row = amgPd.cownnum.astype('category', categories=user_u).cat.codes
        col = amgPd.fullProdName.astype('category', categories=item_u).cat.codes
        
        data = np.array([1 for k in range(len(amgPd))])
        
        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))
        
        df = pd.SparseDataFrame([ pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) 
                                      for i in np.arange(sparse_matrix.shape[0]) ], 
                               index=user_u, columns=item_u, default_fill_value=0)
        finCols = ['cownnum']
        len(finCols)
        finCols.extend(df.columns)
        len(finCols)
        
        dfMtrx = np.empty(shape = (df.shape[0]+1,df.shape[1]+1), dtype=np.ndarray)
        dfMtrx[:1,:][0] = finCols
        dfMtrx[1:,0] = user_u
        dfMtrx[1:,1:] = df.values
        
        np.savetxt(path2+'h1b1_'+premiumFileName[:-4]+"_16_fin.csv", dfMtrx, delimiter=",",fmt='%s')
