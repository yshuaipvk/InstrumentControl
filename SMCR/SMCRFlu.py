import numpy as np
import pandas as pd


# 非负运算
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


import matplotlib.pyplot as plt

data_matrix = pd.read_csv('78-298.csv', header=None)
data_matrix = np.array(data_matrix)
wavelength = data_matrix[:, 0]
# chage wavelength to energe (eV)
# wavelength = 1240 / wavelength
itensity = data_matrix[:, 1:]
temperature = np.arange(78, 308, 10)
itensity = np.transpose(itensity)
LowTemperatureItensity = itensity[:6, :]
LowTemperature = temperature[:6]
# normalized
maxvalues=[]
for i in range(6):
    maxvalue=max(LowTemperatureItensity[i,:])
    maxvalues.append(maxvalue)
LowTemperatureItensity=LowTemperatureItensity/(max(maxvalues))




#PCA
originMatrix=LowTemperatureItensity
U, SV, Vt = np.linalg.svd(originMatrix)
p =3
U = U[:, :p]
SV = np.diag(SV)[:p, :p]
Vt = Vt[:p, :]
V=np.transpose(Vt)

PCAmatrix=U.dot(SV).dot(Vt)
xigema1=residualVariance1(OriginMatrxi=LowTemperatureItensity,PCAMatrix=PCAmatrix,components=p)

def roll(reptimes,xigema,rangeT):
    vaildmatrix = []
    invaildmatrix = []
    for Nrep in range(reptimes):

        t11=-np.random.uniform(rangeT[0,0],rangeT[0,1])
        t12=np.random.uniform(rangeT[1,0],rangeT[1,1])
        t13 = -np.random.uniform(rangeT[2,0], rangeT[2,1])
        t21 = np.random.uniform(rangeT[3,0], rangeT[3,1])
        t22 = -np.random.uniform(rangeT[4,0], rangeT[4,1])
        t23 = np.random.uniform(rangeT[5,0],rangeT[5,1])
        aera1=sum(V[:,0])
        aera2=sum(V[:,1])
        aera3=sum(V[:,2])
        t31=(1-aera1*t11-aera2*t21)/aera3
        t32=(1-aera1*t12-aera2*t22)/aera3
        t33=(1-aera1*t13-aera2*t23)/aera3
        T=np.array([[t11,t12,t13],[t21,t22,t23],[t31,t32,t33]])
        S=V.dot(T)
        nonnegative_S=nonnegative(S)
        ss_1=np.linalg.inv(np.transpose(nonnegative_S).dot(nonnegative_S))
        nonnegative_C=originMatrix.dot(nonnegative_S).dot(ss_1)
        nonnegative_C=nonnegative(nonnegative_C)
        nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
    #C=U.dot(SV).dot(np.linalg.inv(np.transpose(T)))
    #nonnegative_C=nonnegative(C)
    #nonnegativeMatrix=nonnegative_C.dot(np.transpose(nonnegative_S))
        xigema2=residualVariance2(PCAMatrix=PCAmatrix,NonnegativeMatrix=nonnegativeMatrix)
        t=list([xigema2,t11,t12,t13,t21,t22,t23,t31,t32,t33])
        print(Nrep)
        if xigema2<xigema:
            vaildmatrix.append(t)
            print(xigema2)
        else:
            invaildmatrix.append(t)
    vaildmatrix=np.array(vaildmatrix)
    #nvaildmatrix=np.array(invaildmatrix)
    #np.savetxt('tempvaild.csv',vaildmatrix,delimiter=',')
    #np.savetxt('tempinvaild.scv',invaildmatrix,delimiter=',')
#vailddata=np.loadtxt('tempvaild.csv',delimiter=',')
    return vaildmatrix

vdata=np.loadtxt('tempvaild.csv',delimiter=',')
def chooseTrange(vaildmatrix):
    tmatrix=vaildmatrix[:,1:]
    Trange=[]
    for j in range(6):
        tmax=max(tmatrix[:,j])
        tmin=min(tmatrix[:,j])
        print(tmax)
        print(tmin)
        b=list([tmin,tmax])
        Trange.append(b)
    return Trange
new_Trange=chooseTrange(vdata)
print(new_Trange)
T_range0=np.array([[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1]])

for k in range(1):
    vda=roll(10000,0.0001,T_range0)
    new_range=chooseTrange(vda)
    T_range0=new_range
    print(new_range)






'''
U, sv, Vt = np.linalg.svd(itensity)
s = fs
U = U[:, :s]
S = np.diag(sv)[:s, :s]
Vt = Vt[:s, :]
new_itensity = U.dot(S).dot(Vt)
spec = U.dot(S)
temp = S.dot(Vt)

fig=plt.figure(num=1,figsize=(4,8),dpi=80)
ax1=fig.add_subplot(fs,1,1)
ax2=fig.add_subplot(fs,1,2)
ax3=fig.add_subplot(fs,1,fs)
for j in range(s):
    #show total spec
    ax1.plot(wavelength, itensity[:, j],label=temperature[j])
    #show spec
    ax2.plot(wavelength, spec[:, j],label=j)
    #show temp
    ax3.plot(temperature, temp[j, :],'o',label=j)
plt.legend()
#plt.show()
'''
