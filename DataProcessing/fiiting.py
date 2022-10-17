
import numpy as np 
import pandas as pd
import os 
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
root_dir = r"D:\ys\DATA\trce-total\Control-OCVB-trce_2\ion_out.csv"
data = pd.read_csv(root_dir)
data = np.array(data)
i=1
start = 100
stop = 500
x = data[start:stop,0]
y = data[start:stop,i]
def f(x,y0,a1,t1,a2,t2):
    return y0+a1*np.exp(-x/t1) + a2*np.exp(-x/t2)

popt,poc  = curve_fit(f,x,y)
y_ = f(x,*popt)



plt.plot(x,y)
plt.plot(x,y_)
plt.show()