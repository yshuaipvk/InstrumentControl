import numpy as np
import matplotlib.pyplot as plt

#f = np.array([0.001,0.01,0.1,1,10,100,1000,10000,100000])
scale = -4
f = []
for j in range(8):
    for i in range(9):
        F = (i+1)*(10**scale)
        f.append(F)
    scale+=1
f = np.array(f)
w = 2*np.pi*f

print(f)
param = [30000,10e-7,100000,10e-3,10]

def Z_re(x,*param):
    return param[0]/(1+(x*param[0]*param[1])**2)+param[2]/(1+(x*param[2]*param[3])**2)+param[4]


def Z_im(x,*param):
    return (x*param[0]**2*param[1]) / (1 + (x * param[0] * param[1]) ** 2) + \
           (x*param[2]**2*param[3]) / (1 + (x * param[2] * param[3]) ** 2)

z_1 = Z_re(w,*param)
Z_2 = Z_im(w,*param)
plt.plot(z_1,Z_2,'bo')
plt.xlabel("Zre (ohm)")
plt.ylabel("Zim (ohm)")
plt.show()