from re import I
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

# 导入数据,数据为两种染料不同比例的混合物的吸收
data = np.loadtxt(r"D:\ys\python\PythonForScience\SMCR\absorb_demo.txt",delimiter='\t')
# root_dir = r'D:\ys\python\PythonForScience\SMCR\1234.csv'
# data = pd.read_csv(root_dir,header=None)
# data = np.array(data)
# wavelength = data[:,0]
# itensity = data[:,1::2]
# itensity = itensity[:230,:]
# wavelength = wavelength[:230]
wavelength = data[:,0]
itensity = data[:,1:]
# plt.plot(wavelength,itensity[:,1])
U,S,Vt = np.linalg.svd(itensity)
plt.plot(S,'bo')
plt.show()
# 根据S值得到成分数p=2

p = 2

# 新的U，S，Vt矩阵

U =U[:,:p]
S = np.diag(S)
S = S[:p,:p]
Vt = Vt[:p,:]
V = np.transpose(Vt)
SVD_itensity = U.dot(S).dot(Vt)




# def findSeedT(U,V,p):
#     # 随机生成T矩阵
#     t11 = -np.random.uniform(-1, 1)
#     t12 = np.random.uniform(-1, 1)
#     aera1 = sum(V[:, 0])
#     aera2 = sum(V[:, 1])
#     t21 = (1 - aera1 * t11) / aera2
#     t22 = (1 - aera1 * t12) / aera2
#     seed = np.array([t11,t12])
#     T = np.array([[t11, t12], [t21, t22]])
#
#     #T = seed.reshape(p, p)
#     Tt = np.transpose(T)
#     Tt_1 = np.linalg.inv(Tt)
#
#     # 新的光谱矩阵
#     spectrum = V.dot(T)
#     # 新的浓度矩阵
#     concentration = U.dot(S).dot(Tt_1)
#     # 新的强度矩阵
#     D = concentration.dot(np.transpose(spectrum))
#     # 进行非负限制(nn)
#
#     nn_spectrum = nonnegative(spectrum)
#     nn_spectrum_t = np.transpose(nn_spectrum)
#     #StS = nn_spectrum_t.dot(nn_spectrum)
#     #StS_1 = np.linalg.inv(StS)
#     #concentration = D.dot(nn_spectrum).dot(StS_1)
#     nn_concentration = nonnegative(concentration)
#     nn_D = nn_concentration.dot(nn_spectrum_t)
#     sigema_1 = residualVariance1(itensity, SVD_itensity, p)
#     sigema_2 = residualVariance2(SVD_itensity, nn_D)
#     if sigema_1 > sigema_2:
#             out_seed = seed
#     else:
#         out_seed = None
#
#     return out_seed



# seeds =[]
# for i in range(500):
#     # 随机生成T矩阵
#     t11 = -np.random.uniform(-1, 1)
#     t12 = np.random.uniform(-1, 1)
#     aera1 = sum(V[:, 0])
#     aera2 = sum(V[:, 1])
#     t21 = (1 - aera1 * t11) / aera2
#     t22 = (1 - aera1 * t12) / aera2
#     seed = np.array([t11, t12,t21,t22])
#     T = np.array([[t11, t12], [t21, t22]])

#     # T = seed.reshape(p, p)
#     Tt = np.transpose(T)
#     Tt_1 = np.linalg.inv(Tt)

#     # 新的光谱矩阵
#     spectrum = V.dot(T)
#     # 新的浓度矩阵
#     concentration = U.dot(S).dot(Tt_1)
#     # 新的强度矩阵
#     D = concentration.dot(np.transpose(spectrum))
#     # 进行非负限制(nn)

#     nn_spectrum = nonnegative(spectrum)
#     nn_spectrum_t = np.transpose(nn_spectrum)
#     # StS = nn_spectrum_t.dot(nn_spectrum)
#     # StS_1 = np.linalg.inv(StS)
#     # concentration = D.dot(nn_spectrum).dot(StS_1)
#     nn_concentration = nonnegative(concentration)
#     nn_D = nn_concentration.dot(nn_spectrum_t)
#     sigema_1 = residualVariance1(itensity, SVD_itensity, p)
#     sigema_2 = residualVariance2(SVD_itensity, nn_D)
#     if sigema_1 > sigema_2:
#         seeds.append(seed)
#         print(seed)



# T = np.array([-1.890945755119466387e-01,-3.694956145607231068e-01,-1.662793465576301588e-01,2.795726834328388088e-01])

# T = T.reshape(p, p)
# Tt = np.transpose(T)
# Tt_1 = np.linalg.inv(Tt)
# spectrum = V.dot(T)
# concentration = U.dot(S).dot(Tt_1)
# D = concentration.dot(np.transpose(spectrum))
# nn_spectrum = nonnegative(spectrum)
# nn_spectrum_t = np.transpose(nn_spectrum)
# nn_concentration = nonnegative(concentration)
# nn_D = nn_concentration.dot(nn_spectrum_t)

# Tem = 7
# y_1 = nn_concentration[:,0]*nn_spectrum[Tem,0]
# y_2 = nn_concentration[:,1]*nn_spectrum[Tem,1]
# plt.plot(wavelength,y_1)
# plt.plot(wavelength,y_2)
# plt.plot(wavelength,nn_D[:,Tem])
# plt.show()