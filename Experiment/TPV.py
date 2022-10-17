# 简化的TPV测试
# 调节好光强之后，设置文件名称，运行程序，
# 测试TPV，完毕之后自动切换采样电阻测试TPC


from Instrument.LecroyScope import HDO4054A
import numpy as np
import os
from Experiment import experiment_fuction  as ef
import time
import datetime
scope=HDO4054A()
root_dir='D:\\Waveform\\'
now = datetime.datetime.now()
now_day  = now.strftime("%Y%m%d")
now_time = now.strftime("-%H%M%S-")
root = root_dir + now_day
if not os.path.exists(root):
     os.makedirs(root)

voltage=225
#采集TPV数据
scope.configure_sweep(1000)
time.sleep(20)
TPV_filename='TPV'+now_time+str(voltage)+'.txt'
TPV_save_root=os.path.join(root,TPV_filename)
TPV_data=scope.get_waveform('C2')
np.savetxt(TPV_save_root,TPV_data,delimiter=',')
print('TPV saved')
#采集TPC数据
time.sleep(1)
scope.set_couple('C2','D50')
scope.time_base(0.00001,-0.00004,10000)
scope.configure_channel('C2',0.02,-0.06)
time.sleep(10)
TPC_filename='TPC'+ now_time+str(voltage)+'.txt'
TPC_save_root=os.path.join(root,TPC_filename)
TPC_data=scope.get_waveform('C2')
np.savetxt(TPC_save_root,TPC_data,delimiter=',')
print('TPC saved')
time.sleep(1)
scope.configure_channel(channel='C2',volt=0.01,offset=-(voltage+25)/1000)
scope.configure_sweep(2)
scope.time_base(0.002,-0.008,10000)
scope.set_couple('C2','D1M')
#scope.configure_channel('C2',50,-150)