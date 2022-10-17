import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = pd.read_csv("Q-t-fitting.csv", header=None)

data = np.array(data)

x = data[:-7,0]
y = data[:-7,1]

#plt.plot(x,y,'bo')
#plt.semilogx(x,y,'bo')
plt.loglog(x,y,'bo')
plt.show()

def f(x,*param):
    return  param[0] * (( 1 + param[1]* x)**-param[2])

pot,poc = curve_fit(f,x,y,p=[1,1,1])
print(poc)
# new_y = f(x,*pot)
# print(new_y)
# plt.loglog(x,y,'bo')
# #plt.loglog(x,new_y,'bo')
# plt.show()


