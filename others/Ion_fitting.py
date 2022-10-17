# 用于拟合离子迁移动力学数据

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
# 导入数据，OCVD下离子迁移
data = pd.read_table('Ion_dynamic.txt')
data = np.array(data)
x = data[:,0]
y = data[:,1]/max(data[:,1])
#设置公式
def f(t,a,b):
    return a * b * (np.exp(-b * t))

def f1(t,a,b,c):
    return b*np.exp(-a*t)-c*np.exp(a*t)
# #popt拟合参数
popt,pocv = curve_fit(f,x,y,[1,0.1])

# print(popt)
# [6.1233e-05,3.098e-4]
#拟合数据
y_f = f(x,*popt)
#显示数据
plt.semilogx(x,y,'bo',label="origin")
plt.semilogx(x,y_f,label="fitting")
plt.xlabel("t(ms)")
plt.ylabel("Normalized Voltage")
plt.legend()
plt.show()
all_data = []
pcbm_data=[]
# 导入数据
data = pd.read_csv('Vr-t.csv', header=None)
data=np.array(data)
Control_data = data[:,0:2]
PCBM_data = data[:,2:]

def f(t,a,b):
    return a * b * (np.exp(-b * t))
control_x = Control_data[:,0]
control_y = Control_data[:,1]
popt,pocv = curve_fit(f,control_x,control_y,[1,0.1])
control_y_f = f(control_x,*popt)
all_data.append(control_x)
all_data.append(control_y)
all_data.append(control_y_f)

PCBM_x = PCBM_data[:-4,0]
PCBM_y = PCBM_data[:-4,1]
PCBM_popt,PCBM_pocv = curve_fit(f,PCBM_x,PCBM_y,[1,0.1])
PCBM_y_f = f(PCBM_x,*PCBM_popt)

pcbm_data.append(PCBM_x)
pcbm_data.append(PCBM_y)
pcbm_data.append(PCBM_y_f)


pcbm_data = np.array(pcbm_data)
pcbm_data = np.transpose(pcbm_data)
all_data = np.array(all_data)
all_data=np.transpose(all_data)
print(popt)
print(PCBM_popt)
# np.savetxt("Control_fit.txt",all_data,delimiter=',')
# np.savetxt("PCBM_fit.txt",pcbm_data,delimiter=',')

#
# data=pd.read_csv("demo.csv",header=None)
# data = np.array(data)
#
# d_x = data[:,0]
# d_y = data[:,1]
# data_1 = pd.read_csv("wd600.csv",header=None)
# data_1 = np.array(data_1)
#
# w_x = data_1[:,0]
# w_y = data_1[:,1]
#
# # plt.plot(w_x,w_y)
# # plt.show()
# def f(x,a,b,c,d,e):
#     return a+b*x**2+c*x**3+d*x**4+e*x**5
# #拟合标准数据
# d_popt,d_popc = curve_fit(f,d_x,d_y,p0=[-0.9,0.00243,-3.3435E-6,2.892E-9,-1.04058E-12,])
# d_y_f = f(d_x,*d_popt)
#
# # plt.plot(d_x,d_y,'bo')
# # plt.plot(d_x,d_y_f)
# # plt.show()
#
# #拟合实验数据
# # w_popt,e_popc = curve_fit(f,w_x,w_y,p0=[-0.9,0.00243,-3.3435E-6,2.892E-9,-1.04058E-12,])
# # w_y_f = f(w_x,*w_popt)
#
#
# new_w_y = f(w_x,*d_popt)
#
# k = w_y/new_w_y
# saved_data =[]
# saved_data.append(w_x)
# saved_data.append(k)
# saved_data=np.transpose(np.array(saved_data))
# np.savetxt('k.txt',saved_data,delimiter=',')
# # plt.plot(w_x,k,'bo')
# # plt.show()
#



