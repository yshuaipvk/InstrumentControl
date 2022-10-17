"""
用于测量改变光强下的OCVD-TRCE-Ion
测量OCVD时,设置时基为 1 s,触发为 C1，下降沿触发
测量TRCE时，设置时基为 50 us,触发设置为C3，上升沿触发
测量Ion时，设置时基为50 ms，触发这只为C3，下降沿触发
"""

from Instrument.LecroyScope import HDO4054A
from Instrument.DG535 import DG
import Experiment.experiment_fuction as ef
import time
import numpy as np
import os
scope = HDO4054A()
dg535 = DG()
data = ef.get_data()

"""
设置实验参数：
rate: 设置实验频率(HZ),根据光照之后电池电压衰减到0的时间设置，一般50s能衰减到0
light_on: 设置光照时间(s)，根据光照后达到稳定电压的时间设置，一般为 10 
extract_time: 设置抽取时间(s)
root_dir: 保存路径，为当前日期
file_describe: 文件命名
"""
rate = 0.02
light_on = 10
extract_time = 0.00002
root_dir = "D:\ys\DATA\\"+data
file_describe = "describe"



# 测量OCVD
dg535.set_time_delay(rate,light_on,0,extract_time)
print("OCVD start ....")
scope.configure_channel('C2',0.1,-0.3)
scope.time_base(1,-4,10000)
scope.configure_sample_mode('RealTime')
scope.configure_trigger_source('C1')
scope.configure_trigger_slope('C1',2)
scope.clear_sweep()
scope.configure_sweep(3)
time.sleep(4/rate)  #等待采集数据，数据平均三次，等待4个周期，舍弃第一个周期数据
ocvd_data = scope.get_waveform('C2')
ocvd_file_name = file_describe+'-ocvd.txt'
ocvd_fn = os.path.join(ocvd_file_name,root_dir)
np.savetxt(ocvd_fn,ocvd_data,delimiter=',')
scope.configure_sweep(1)
time.sleep(1)
# 测量 TRCE

print("Trce start ....")
scope.configure_trigger_source('C3')
scope.configure_trigger_slope('C3',1)
scope.time_base(0.00005,-0.0002,10000)
scope.configure_sweep(3)
scope.clear_sweep()
time.sleep(4/rate)
trce_data = scope.get_waveform('C2')
trce_file_name = file_describe+'trce.txt'
trce_fn = os.path.join(trce_file_name,root_dir)
np.savetxt(trce_fn,trce_data)
scope.configure_sweep(1)
time.sleep(1)


#测量Ion
print("Ion start ....")
scope.configure_trigger_slope('C3',2)
scope.time_base(0.05,-0.2,10000)
scope.configure_sweep(4)
scope.clear_sweep()
time.sleep(4/rate)
trce_data = scope.get_waveform('C2')
ion_file_name = file_describe+'ion.txt'
ion_fn = os.path.join(ion_file_name,root_dir)
np.savetxt(trce_fn,trce_data)
time.sleep(1)

print("Completed, please change light itensity")





