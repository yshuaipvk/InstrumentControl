import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#Extract data into numpy arrays
lambda_1 = []
lambda_2 = []
# t 为时间序列
# g 为仪器测量到的信号
# f为仪器响应函数
t =[]
f = []
g = []
#Definition of the function
def convol(x,A,B,C):
    dx=x[1]-x[0]
    return A*np.convolve(f, np.exp(-lambda_1*x))[:len(x)]*dx+B*np.convolve(f, np.exp(-lambda_2*x))[:len(x)]*dx+C

#Determination of fit parameters A,B,C
popt, pcov = curve_fit(convol, t, g)
A,B,C= popt
perr = np.sqrt(np.diag(pcov))

#Plot fit
fit = convol(t,A,B,C)
plt.plot(t, fit)
plt.scatter(t, g,s=50, color='black')
plt.show()