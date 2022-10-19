from logging import root
import Experiment.experiment_fuction as ef
from Instrument.LecroyScope import HDO4054A
from Instrument.DG535 import DG
import numpy as np
from Instrument.resistance import M642
from Instrument.switch import Switch
import os
import time
from Instrument.tenpuratuer import TC202
np.set_printoptions(suppress=True)



#           _
#       .__(.)< (MEOW)
#        \___)   
# ~~~~~~~~~~~~~~~~~~


DG535 = DG()  # DG4535
SCOPE_1 = HDO4054A(address="TCPIP0::169.254.75.166::inst0::INSTR")  # 示波器
SCOPE_2 = HDO4054A(address="TCPIP0::169.254.75.166::inst0::INSTR")
# m642 = M642()                             # 电阻箱
# tems_ins = TC202(address='COM14')         # 恒温器
# SCOPE_2  = HDO4054A(address="")
# sw = Switch('COM12')                      # 继电器开关


RATE = 0.025       # 实验频率
LIGHT_TIME = 12    # 光照时间
EXTRACT_TIME = 0.00002    # 抽取时间
ROOT_DIR = r"D:\Waveform\YS\DSSC"    # 保存路径

# 创建 文件夹
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

# data = ef.get_data()  

file_describe = ""
time_delay_list = [1e-6,2e-6,5e-6,8e-6,1e-5,2e-5,5e-5,8e-5,0.0001,0.00002,0.0005,0.0008,0.001,0.002,0.005,
                       0.01,0.02,0.05,0.08,0.1,0.2,0.5,0.8,1,2,3,5,8,10]

def OCVB(timeBases=[0.001,0.01,1]):
    for timeBase in timeBases:
        ef.OCVB(scope=SCOPE_1,dg535=DG535,dg_rate=RATE,light_time=LIGHT_TIME,file_desc=file_describe,root_dir=ROOT_DIR,time_base=timeBase,sweeps=3)

def OCVD(timeBases=[0.001,0.01,1]):
    for timeBase in timeBases:
        ef.OCVD(scope=SCOPE_1, dg535=DG535, dg_rate=RATE, light_time=LIGHT_TIME, file_desc=file_describe, root_dir=ROOT_DIR,time_base=timeBase,sweeps=3)
 
def OCVDTrce(timeDelayList,trce=True,ion=False):
    for timeDelay in timeDelayList:
        print("Change time delay to "+str(timeDelay))
        file_desc =file_describe+str(timeDelay)
        if trce:
            ef.OCVD_trce(scope=SCOPE_1,dg535=DG535,dg_rate=RATE,light_time=LIGHT_TIME,time_base=0.00002,time_delay=timeDelay,
                  extract_time=EXTRACT_TIME,file_desc=file_desc,root_dir=ROOT_DIR)
        if ion:
            ef.OCVD_ion(scope=SCOPE_1, dg535=DG535, dg_rate=RATE, light_time=LIGHT_TIME, time_base=0.002,
                    time_delay=timeDelay, extract_time=EXTRACT_TIME, file_desc=file_desc, root_dir=ROOT_DIR)

def OCVBTrce(timeDelayList,trce=True,ion=False):
    for timeDelay in timeDelayList:
        print("Change time delay to "+str(timeDelay))
        file_desc =file_describe+str(timeDelay)
        if trce:
            ef.OCVB_trce(scope=SCOPE_1,dg535=DG535,dg_rate=RATE,light_time=timeDelay,time_base=0.00002,
                     extract_time=EXTRACT_TIME,file_desc=file_desc,root_dir=ROOT_DIR)

        if ion:
            ef.OCVB_ion(scope=SCOPE_1, dg535=DG535, dg_rate=RATE, light_time=timeDelay, time_base=0.002,
                     extract_time=EXTRACT_TIME, file_desc=file_desc, root_dir=ROOT_DIR)
def doubleTest(timeDelayList):
    for timeDelay in timeDelayList:
        print("Change time delay to "+str(timeDelay))
        file_desc =file_describe+str(timeDelay)
        ef.CsTPTDoubleTest(scope1=SCOPE_1,scope2=SCOPE_2,dg535=DG535,dg_rate=RATE,light_time=timeDelay,time_base_1=5E-5,
                           time_base_2=0.002,extract_time=EXTRACT_TIME,file_desc=file_desc,root_dir=ROOT_DIR,)



if __name__ == '__main__':

    # OCVB(timeBases=[0.001,0.01,1])
    # OCVD(timeBases=[0.001,0.01,1])
    OCVBTrce(timeDelayList=time_delay_list,trce=True,ion=True)
    OCVDTrce(timeDelayList=time_delay_list,trce=True,ion=True)
    doubleTest(timeDelayList=time_delay_list)
    



