"""
二次抽取：
在电压回复的最高点进行二次抽取

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root_dir = r"C:\Users\SDMM\Desktop\20200825\PCBM0.1ion.txt"

data = pd.read_csv(root_dir,delimiter=' ')

data = np.array(data)

def get_max_recovery_time(ion_data):
    """get the max voltage recovery max time
    :param ion_data:
    :return:
    """
    mask = (ion_data[:,0]>=0)
    y = ion_data[mask,1]
    _voltage_recovery = np.max(y)
    mask_ = (ion_data[:,1]==_voltage_recovery)
    return data[mask_,0][-1]

"""
用于测量不同衰减时间下的OCVD-TRCE-Ion
测量OCVD时,设置时基为 1 s,B口接C1触发为 C1，下降沿触发
测量TRCE时，设置时基为 50 us,C口接C1，触发设置为C1，上升沿触发
测量Ion时，设置时基为50 ms，触发设置为C1，下降沿触发
"""
from Instrument.LecroyScope import HDO4054A
from Instrument.DG535 import DG
import Experiment.experiment_fuction as ef
import time
import numpy as np
import os


"""
设置实验参数：
rate: 设置实验频率(HZ),根据光照之后电池电压衰减到0的时间设置，一般50s能衰减到0
light_on: 设置光照时间(s)，根据光照后达到稳定电压的时间设置，一般为 10 
extract_time: 设置抽取时间(s)
root_dir: 保存路径，为当前日期
file_describe: 文件命名
"""




def OCVD(scope,dg535,dg_rate,light_time,file_desc,root_dir,time_base):
    """
    测量OCVD
    :param : dg_rate, configure DG535 rate
    :param : light_set,set light on time
    :param : file_desc, set deacribion for saved file
    :param : root_dir , saveing root
    :param : time_base, unit second(s)
    """
    dg535.set_time_delay(dg_rate,light_time,0,0)
    print("OCVD start ....")
    scope.configure_channel('C2',0.2,-0.6)
    scope.time_base(time_base,-4*time_base,10000)
    #scope.time_base(1,-4,10000)
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.configure_trigger_slope('C1',2)
    scope.clear_sweep()
    scope.configure_sweep(3)
    time.sleep(4/dg_rate)  #等待采集数据，数据平均三次，等待4个周期，舍弃第一个周期数据
    ocvd_data = scope.get_waveform('C2')
    ocvd_file_name = file_desc+str(time_base)+'s-ocvd.txt'
    ocvd_fn = os.path.join(root_dir,ocvd_file_name)
    print(ocvd_fn)
    np.savetxt(ocvd_fn,ocvd_data,delimiter=',')
    scope.configure_sweep(1)
    print("OCVD done")


def trce(scope,dg535,dg_rate,light_time,time_delay,extract_time,file_desc,root_dir):
    """
    TRCE test
    :param : dg_rate, configure DG535 rate
    :param : light_set,set light on time
    :param : file_desc, set deacribion for saved file
    :param : root_dir , saveing root
    """
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    print("Trce start ....")
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.configure_trigger_slope('C1', 1)
    scope.time_base(0.00005, -0.0002, 10000)
    scope.configure_sweep(3)
    scope.clear_sweep()
    time.sleep(4 / dg_rate)
    trce_data = scope.get_waveform('C2')
    trce_file_name = file_desc + 'trce.txt'
    trce_fn = os.path.join(root_dir,trce_file_name)
    np.savetxt(trce_fn, trce_data,delimiter=',')
    print("Save file to "+trce_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    time.sleep(0.5)


def ion(scope,dg535,dg_rate,light_time,time_delay,extract_time,file_desc,root_dir):
    """
     ion test
     :param: scope , scope object
     :param: dg535 , dg535 object
     :param: dg_rate, configure DG535 rate
     :param: light_time,set light on time
     :param: file_desc, set deacribion for saved file
     :param: root_dir , saveing root
     :param: extract_time . recommand to 20 us
     :param: time_delay , dark_time befrore extract
     """
    print("Ion start ....")
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    scope.configure_trigger_slope('C1', 2)
    scope.time_base(0.05, -0.2, 10000)
    scope.configure_sweep(4)
    scope.clear_sweep()
    time.sleep(4 / dg_rate)
    ion_data = scope.get_waveform('C2')
    ion_file_name = file_desc + 'ion.txt'
    ion_fn = os.path.join(root_dir,ion_file_name)
    np.savetxt(ion_fn, ion_data,delimiter=',')
    print("Save ion file to"+ ion_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    time.sleep(0.5)
    return ion_data

def second_extract(scope,dg535,dg_rate,light_time,time_delay,extract_time,file_desc,root_dir,):
    """ secondary extract
    :param scope:
    :param dg535:
    :param dg_rate:
    :param light_time:
    :param time_delay:
    :param extract_time:
    :param file_desc:
    :param root_dir:
    :return:
    """
    print("Secondary extract start.....")
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    scope.configure_trigger_slope('C1', 2)
    scope.time_base(0.05, -0.2, 10000)
    scope.configure_sweep(4)
    scope.clear_sweep()
    time.sleep(4 / dg_rate)
    ion_data = scope.get_waveform('C2')
    ion_file_name = file_desc + 'secondary_extract.txt'
    ion_fn = os.path.join(root_dir, ion_file_name)
    np.savetxt(ion_fn, ion_data, delimiter=',')
    print("Save ion file to" + ion_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    time.sleep(0.5)



if __name__ == '__main__':
    DG535 = DG()
    SCOPE = HDO4054A()
    data = ef.get_data()
    # 设置实验超参数
    RATE = 0.025
    LIGHT_TIME = 10
    EXTRACT_TIME = 0.00004
    ROOT_DIR = "D:\\Waveform\\" + data
    TIME_BASE_1 = 1
    TIME_BASE_2 = 0.001
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
    file_describe = "PCBM-"


    time_delay_list = [0,0.000001,0.000002,0.000005,0.000008,
                       0.00001,0.00002,0.00005,0.00008,
                       0.0001,0.0002,0.0005,0.0008,
                       0.001,0.002,0.005,0.008,
                       0.1,0.2,0.5,0.8]

    # OCVD(scope=SCOPE, dg535=DG535, dg_rate=RATE,light_time=LIGHT_TIME, file_desc=file_describe, root_dir=ROOT_DIR,time_base=TIME_BASE_1)
    # OCVD(scope=SCOPE, dg535=DG535, dg_rate=RATE, light_time=LIGHT_TIME, file_desc=file_describe, root_dir=ROOT_DIR,
    #         time_base=TIME_BASE_2)



    print('Begin to change time delay')
    for TIME_DELAY in time_delay_list:
        print("Change time delay to "+str(TIME_DELAY))
        file_desc =file_describe+str(TIME_DELAY)
        trce(scope=SCOPE,dg535=DG535,dg_rate=RATE,light_time=LIGHT_TIME,time_delay=TIME_DELAY,
             extract_time=EXTRACT_TIME,file_desc=file_desc,root_dir=ROOT_DIR)

        time.sleep(1)
        data = ion(scope=SCOPE, dg535=DG535, dg_rate=RATE, light_time=LIGHT_TIME, time_delay=TIME_DELAY,
             extract_time=EXTRACT_TIME, file_desc=file_desc, root_dir=ROOT_DIR)
        
        second_time_delay  = get_max_recovery_time(data)+TIME_DELAY
        time.sleep(1)
        second_extract(scope=SCOPE, dg535=DG535, dg_rate=RATE, light_time=LIGHT_TIME, time_delay=TIME_DELAY,
             extract_time=EXTRACT_TIME, file_desc=file_desc, root_dir=ROOT_DIR)



