
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#np.set_printoptions(suppress=True)
def nonnegative(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i][j] = max(matrix[i][j], 0)
    return matrix


def residualVariance1(OriginMatrxi, PCAMatrix, components):
    ResidualVariance_1 = 0
    m, n = OriginMatrxi.shape[0], OriginMatrxi.shape[1]

    for i in range(m):
        for j in range(n):
            ResidualVariance_1 += (OriginMatrxi[i][j] - PCAMatrix[i][j]) ** 2
    return ResidualVariance_1 / ((m - components) * (n - components))


def residualVariance2(PCAMatrix, NonnegativeMatrix):
    ResidualVariance2 = 0
    m, n = PCAMatrix.shape[0], PCAMatrix.shape[1]
    for i in range(m):
        for j in range(n):
            ResidualVariance2 += (PCAMatrix[i][j] - NonnegativeMatrix[i][j]) ** 2
    return ResidualVariance2 / (m * n)
def NormalizeMatrix(originMatrix):
    for sampleNumber in range(originMatrix.shape[0]):
        spec=originMatrix[sampleNumber,:]
        originMatrix[sampleNumber,:]=spec/max(spec)
    return originMatrix
# 导入数据

data = np.loadtxt('absorb_demo.txt')

wavelength = data[:, 0]
od = data[:, 1:]

originMatrix=np.transpose(od)
#originMatrix=NormalizeMatrix(originMatrix)
U,SV,Vt=np.linalg.svd(originMatrix)
k=2
U=U[:,:k]
SV=np.diag(SV)[:k,:k]
Vt=Vt[:k,:]
PCAMatrix=U.dot(SV).dot(Vt)
xigema1=residualVariance1(OriginMatrxi=originMatrix,PCAMatrix=PCAMatrix,components=k)
P_matrix = []
V=np.transpose(Vt)



vaildmatrix=[]
invaildmatrix=[]
for Nrep in range(100000):
    t11=-np.random.uniform(-1,1)
    t12=np.random.uniform(-1,1)
    aera1=sum(V[:,0])
    aera2=sum(V[:,1])
    t21=(1-aera1*t11)/aera2
    t22=(1-aera1*t12)/aera2
    T=np.array([[t11,t12],[t21,t22]])

    S = V.dot(T)

    nonnegative_S=nonnegative(S)
    ss_1=np.linalg.inv(np.transpose(nonnegative_S).dot(nonnegative_S))
    nonnegative_C=originMatrix.dot(nonnegative_S).dot(ss_1)
    nonnegative_C=nonnegative(nonnegative_C)
    nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
    #C=U.dot(SV).dot(np.linalg.inv(np.transpose(T)))
    #nonnegative_C=nonnegative(C)
    nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
    xigema2=residualVariance2(PCAMatrix=PCAMatrix,NonnegativeMatrix=nonnegativeMatrix)
    t=list([xigema2,t11,t12,t21,t22])
    if xigema2<xigema1:
        vaildmatrix.append(t)
        print(xigema2)
    else:
        invaildmatrix.append(t)
vaildmatrix=np.array(vaildmatrix)
invaildmatrix=np.array(invaildmatrix)
np.savetxt('vaild.csv',vaildmatrix,delimiter=',')
#np.savetxt('invaild.scv',invaildmatrix,delimiter=',')


# vailddata=np.loadtxt('vaild.csv',delimiter=',')
# #invailddata=np.loadtxt('invaild.scv',delimiter=',')
# import matplotlib.pyplot as plt
# #plt.plot(vailddata[:,1],vailddata[:,2],'o',c='black',label='valid')
# #plt.plot(invailddata[:1000,1],invailddata[:1000,2],'o',c='red',label='invalid')
#
# a=vailddata[9,:]
# t11=a[1]
# t12=a[2]
# t21=a[3]
# t22=a[4]
# T=np.array([[t11,t12],[t21,t22]])
# S=V.dot(T)
# nonnegative_S=nonnegative(S)
# ss_1=np.linalg.inv(np.transpose(nonnegative_S).dot(nonnegative_S))
# nonnegative_C=originMatrix.dot(nonnegative_S).dot(ss_1)
# nonnegative_C=nonnegative(nonnegative_C)
# nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
# #C=U.dot(SV).dot(np.linalg.inv(np.transpose(T)))
# #nonnegative_C=nonnegative(C)
# #nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
# St=np.transpose(nonnegative_S)
# P1=nonnegative_C[0][0]*St[0,:]
# P2=nonnegative_C[0][1]*St[1,:]
# plt.plot(wavelength,originMatrix[0,:],'o',label='origin')
# plt.plot(wavelength,nonnegativeMatrix[0,:],label='new')
# plt.plot(wavelength,P1,'--',label='component 1')
# plt.plot(wavelength,P2,'--',label='component 2')
# plt.xlabel('wavelength')
# plt.ylabel('itensity')
# plt.legend()
# plt.show()