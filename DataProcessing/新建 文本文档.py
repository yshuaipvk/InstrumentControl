import numpy as np 
import os
wave_dir = r"C:\Users\ys\Documents\WeChat Files\wxid_1gx7h791samv22\FileStorage\File\2022-07\680-78 K.dat"   # 光谱
dyna_dir = r"C:\Users\ys\Documents\WeChat Files\wxid_1gx7h791samv22\FileStorage\File\2022-07\680-78-KINETIC.dat"   #动力学
save_dir = r"2233.txt"   #保存路径
wave = np.loadtxt(wave_dir,delimiter = "\t")
dyna = np.loadtxt(dyna_dir,delimiter = "\t")

wave = wave[:,1]
wave_length = wave.shape[0]
wave = wave.reshape(wave_length,1)

dyna = dyna[:,1]
dyna_length = dyna.shape[0]

dyna = dyna.reshape(1,dyna_length)

out =wave.dot(dyna)
np.savetxt(X=out,fname=save_dir,delimiter=',',fmt=)
