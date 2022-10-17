from re import X
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import os 

# root_dir = r'D:\ys\python\PythonForScience\SMCR\bcor-agg-78k.txt'

# data = pd.read_table(root_dir,delimiter='\t',skiprows=22,header=None)
# print(data)
# data = np.array(data)
# x = data[:,0]
# y = data[:,1]
# plt.plot(x,y)
# plt.show()

root_dir = r'D:\ys\python\PythonForScience\SMCR\1234.csv'
data = pd.read_csv(root_dir,header=None)
data = np.array(data)
x = data[:,0]
y = data[:,1::2]

# wavelength = data[:,0]
# itensity = data[:,1:]

# U,S,Vt = np.linalg.svd(itensity)
# p=2 

# U = U[:,:p]
# S = np.diag(S)
# S = S[:p,:p]
# Vt = Vt[:p,:]

# SVD_itensity = U.dot(S).dot(Vt)
