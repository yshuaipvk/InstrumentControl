import numpy as np
from scipy.optimize import curve_fit
import os
import re
import  matplotlib.pyplot as plt

def f(_x,y0,A1,t1,A2,t2):
    return y0+A1*np.exp(-_x/t1)+ A2*np.exp(-_x/t2)



root_dir =  r"C:\Users\SDMM\Desktop\20201112-li"

file_names = os.listdir(root_dir)
print(file_names)
baseline_dir = os.path.join(root_dir,file_names[0])
baseline = np.loadtxt(baseline_dir,delimiter=',',skiprows=5)
baseline_y = baseline[:,1]
baseline_y = baseline_y-np.average(baseline_y[200:500])

for file_name in file_names:
    if not re.findall("bseline",file_name) and re.findall('TPC',file_name):
        file_dir = os.path.join(root_dir,file_name)
        data = np.loadtxt(file_dir,delimiter=',',skiprows=5)
        x = data[:,0]
        y = data[:,1]-baseline_y
        y = y-np.average(y[200:500])
        #y = y/max(y)
        plt.plot(x,y)

plt.show()





#plt.show()
# output = []
# for i in range(2):
#     file_name = file_names[i]
#     if re.findall("TPV",file_name):
#         file_dir = os.path.join(root_dir,file_name)
#         data = np.loadtxt(file_dir,delimiter=',',skiprows=5)
#         x = data[:,0]
#         y = data[:,1]
#
#         baseline = np.average(y[100:500])
#         baseline_y = y - baseline
#         normalized_y = baseline_y - np.max(baseline_y)
#         x = x[1003:]
#         normalized_y = normalized_y[1003:]
#         plt.plot(x, normalized_y,'bo')
#         popt,poc = curve_fit(f,xdata=x,ydata=normalized_y)
#
#         output.append(popt)
#
# print(output)
# plt.show()




