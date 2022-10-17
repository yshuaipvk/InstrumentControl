import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

root_dit = r"D:\Waveform\20200924"

fns  = os.listdir(root_dit)
processed_data = []
for i in range(len(fns)):
    fn = fns[i]
    if re.findall('light',fn):
        fn_dir = os.path.join(root_dit,fn)
        data = np.loadtxt(fn_dir,delimiter=',')
        #plt.plot(data[:,0],data[:,1],label = fn)
        light_on_time = float(fn[12:-4])
        max_voltage = max(data[:,1])
        processed_data.append((light_on_time,max_voltage))
# plt.xlabel("t (s)")
# plt.ylabel("Vrecovery (V)")
# plt.legend()
# plt.show()
print(processed_data)
#np.savetxt("1.txt",processed_data,delimiter=',')
