import numpy as np
import matplotlib.pyplot as plt
od=np.loadtxt('OD.dat')
time=np.loadtxt('timevect.dat')
wave=np.loadtxt('waverect.dat')
U,S,Vt=np.linalg.svd(od)
k=3
S=np.diag(S)
U=U[:,:k]
S=S[:k,:k]
Vt=Vt[:k,:]

f_1=np.loadtxt('4\\1f')
f_2=np.loadtxt('4\\2f')
f_3=np.loadtxt('4\\3f')
Vt_new=[]
Vt_new.append(f_1[:,0])
Vt_new.append(f_2[:,0])
Vt_new.append(f_3[:,0])
Vt_new=np.array(Vt_new)

C=S.dot(Vt_new)

data_new=U.dot(S).dot(C)
data_1=U.dot(S)

