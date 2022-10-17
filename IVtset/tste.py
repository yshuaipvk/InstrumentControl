import numpy as np
import matplotlib.pyplot as plt


x =  np.arange(0,100,1)
y = 0.8 * x +0.1
error = 5*np.random.randn(100)
y = y+error
plt.plot(x,y,'bo',label="origin data")
plt.plot(x,0.8*x+0.1, label="fitting curve")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
