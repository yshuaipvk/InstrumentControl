# 一些简化的功能函数


import datetime
import time
import numpy as np
import os
import math

from pandas import date_range


np.set_printoptions(suppress=True)
# 获取当前日期，并转化为20200101格式
def get_data():
    now_time = datetime.datetime.now().strftime("%Y%m%d")
    return now_time


"""
用于测量不同衰减时间下的OCVD-TRCE-Ion，OCVB-TRCE-Ion
测量OCVB时，继电器开关打开，B口接C1，触发设置为C1，上升沿触发
测量OCVD时，继电器开关打开，B口接C1，触发设置为C1，下降沿触发
测量TRCE时，继电器开关关闭，C口接C1，触发设置为C1，上升沿触发
测量Ion时，继电器开关关闭，触发设置为C1，下降沿触发
rate: 设置实验频率(HZ),根据光照之后电池电压衰减到0的时间设置，一般50s能衰减到0
light_on: 设置光照时间(s)，根据光照后达到稳定电压的时间设置，一般为 10 
extract_time: 设置抽取时间(s)
root_dir: 保存路径，为当前日期
file_describe: 文件命名
"""


def OCVB(scope,dg535,dg_rate,light_time,file_desc,root_dir,time_base,sweeps=3):
    """
    OCVB measurement
    :param : dg_rate, configure DG535 rate
    :param : light_set,set light on time
    :param : file_desc, set deacribion for saved file
    :param : root_dir , saveing root
    :param : time_base, unit second(s)
    """
    dg535.set_time_delay(dg_rate,light_time,0,0)
    print("OCVB start ....")
    scope.configure_channel('C2',0.2,-0.6)
    scope.time_base(time_base,-4*time_base,10000)
    #scope.time_base(1,-4,10000)
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.configure_trigger_slope('C1',1)
    scope.clear_sweep()
    scope.configure_sweep(sweeps)
    time.sleep(4/dg_rate)  #等待采集数据，数据平均三次，等待4个周期，舍弃第一个周期数据
    ocvb_data = scope.get_waveform('C2')
    ocvb_file_name = file_desc + '-'+str(time_base)+'-OCVB.txt'
    ocvb_fn = os.path.join(root_dir,ocvb_file_name)
    np.savetxt(ocvb_fn,ocvb_data,delimiter=',')
    scope.configure_sweep(1)
    print("Save file to "+ ocvb_fn)
    print("OCVB done")
    print('------------------------------')

def OCVD(scope,dg535,dg_rate,light_time,file_desc,root_dir,time_base,sweeps=3):
    """
    OCVD measurement
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
    scope.configure_sweep(sweeps)
    time.sleep(4/dg_rate)  #等待采集数据，数据平均三次，等待4个周期，舍弃第一个周期数据
    ocvd_data = scope.get_waveform('C2')
    ocvd_file_name = file_desc+ '-' + str(time_base)+'-OCVD.txt'
    ocvd_fn = os.path.join(root_dir,ocvd_file_name)
    np.savetxt(ocvd_fn,ocvd_data,delimiter=',')
    scope.configure_sweep(1)
    print("Save file to "+ocvd_fn)
    print("OCVD done")
    print('------------------------------')

def OCVB_trce(scope,dg535,dg_rate,light_time,time_base,extract_time,file_desc,root_dir,sweeps=3):
    """
    OCVB-TRCE measurement
    :param ：scope.clsss
    :param : dg535,class
    :param : dg_rate, configure DG535 rate
    :param : light_time
    :param : time_base
    :param : file_desc, set deacribion for saved file
    :param : root_dir , saveing root
    """
    # OCVB-Trce时，开始抽取时间和光照时间一致，则 C=B+0
    dg535.set_time_delay(dg_rate, light_time, 0, extract_time)
    print("OCVB Trce start ....")
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.configure_trigger_slope('C1', 1)
    scope.time_base(time_base, -4 * time_base, 10000)
    scope.configure_sweep(sweeps)
    scope.clear_sweep()
    time.sleep((sweeps+1) / dg_rate)
    trce_data = scope.get_waveform('C2')
    trce_file_name = file_desc + '-' + str(time_base)+'-OCVB_trce.txt'
    trce_fn = os.path.join(root_dir,trce_file_name)
    np.savetxt(trce_fn, trce_data,delimiter=',')
    print("Save file to "+trce_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    print('-----------------------')

def OCVD_trce(scope,dg535,dg_rate,light_time,time_delay,time_base,extract_time,file_desc,root_dir,sweeps=3):
    """
    ocvd-trce measurement
    :param : dg_rate, configure DG535 rate
    :param : light_set,set light on time
    :param : file_desc, set deacribion for saved file
    :param : root_dir , saveing root
    """
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    print("OCVD-Trce start ....")
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.configure_trigger_slope('C1', 1)
    scope.time_base(time_base, -4 * time_base, 10000)
    scope.configure_sweep(sweeps)
    scope.clear_sweep()
    time.sleep((sweeps+1) / dg_rate)
    trce_data = scope.get_waveform('C2')
    trce_file_name = file_desc + '-'+str(time_base)+ '-OCVD_trce.txt'
    trce_fn = os.path.join(root_dir,trce_file_name)
    np.savetxt(trce_fn, trce_data,delimiter=',')
    print("Save file to "+trce_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    print('------------------------------')

def OCVB_ion(scope,dg535,dg_rate,light_time,time_base,extract_time,file_desc,root_dir,sweeps=3):
    """
     OCVB-ion measurement
     :param: scope , scope object
     :param: dg535 , dg535 object
     :param: dg_rate, configure DG535 rate
     :param: light_time,set light on time
     :param: file_desc, set deacribion for saved file
     :param: root_dir , saveing root
     :param: extract_time . recommand to 20 us
     :param: time_delay , dark_time befrore extract
     """
    print("OCVB-Ion start ....")
    dg535.set_time_delay(dg_rate, light_time, 0, extract_time)
    scope.configure_trigger_slope('C1', 2)
    scope.time_base(time_base, -4*time_base, 10000)
    scope.configure_sweep(sweeps)
    scope.clear_sweep()
    time.sleep((sweeps+1) / dg_rate)
    trce_data = scope.get_waveform('C2')
    ion_file_name = file_desc +"-"+str(time_base)+ '-OCVB_ion.txt'
    ion_fn = os.path.join(root_dir,ion_file_name)
    np.savetxt(ion_fn, trce_data,delimiter=',')
    print("Save ion file to "+ ion_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    print('------------------------------')

def OCVD_ion(scope,dg535,dg_rate,light_time,time_delay,time_base,extract_time,file_desc,root_dir,sweeps=3):
    """
     iocvd-ion measurement
     :param: scope , scope object
     :param: dg535 , dg535 object
     :param: dg_rate, configure DG535 rate
     :param: light_time,set light on time
     :param: file_desc, set deacribion for saved file
     :param: root_dir , saveing root
     :param: extract_time . recommand to 20 us
     :param: time_delay , dark_time befrore extract
     """
    print("OCVD Ion start ....")
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    scope.configure_trigger_slope('C1', 2)
    scope.time_base(time_base, -4*time_base, 10000)
    scope.configure_sweep(sweeps)
    scope.clear_sweep()
    time.sleep((sweeps+1) / dg_rate)
    trce_data = scope.get_waveform('C2')
    ion_file_name = file_desc +'-'+str(time_base)+'-OCVD_ion.txt'
    ion_fn = os.path.join(root_dir,ion_file_name)
    np.savetxt(ion_fn, trce_data,delimiter=',')
    print("Save ion file to "+ ion_fn)
    time.sleep(0.5)
    scope.configure_sweep(1)
    print('------------------------------')

def OcvDoubleTest(scope1,scope2,dg535,dg_rate,light_time,file_desc,root_dir,time_base_1,time_base_2,sweeps=3):
    """
    measure OCVB and OCVD in one test by two scope
    """
    # 示波器1用于采集OCVD信号
    dg535.set_time_delay(dg_rate,light_time,0,0)
    scope1.configure_channel('C2',0.2,-0.6)
    scope1.time_base(time_base_1,-4*time_base_1,10000)
    scope1.configure_sample_mode('RealTime')
    scope1.configure_trigger_source('C1')
    scope1.configure_trigger_slope('C1',2)  #下降沿触发，用于采集OCVD
    scope1.clear_sweep()
    scope1.configure_sweep(sweeps)

    # 示波器2用于采集OCVB信号
    scope2.configure_channel('C2',0.2,-0.6)
    scope2.time_base(time_base_2,-4*time_base_2,10000)
    scope2.configure_sample_mode('RealTime')
    scope2.configure_trigger_source('C1')
    scope2.configure_trigger_slope('C1',1)   #上升沿触发，采集OCVB
    scope2.clear_sweep()
    scope2.configure_sweep(sweeps)
    
    time.sleep((sweeps+1)/dg_rate)

    # 获取数据
    ocvb_data  = scope2.gwt_waveform("C2")
    ocvd_data  = scope1.get_waveform("C2")
    ocvb_file_name = file_desc+ '-' + str(time_base_1)+'-OCVD.txt'
    ocvb_fn = os.path.join(root_dir,ocvb_file_name)
    
    ocvd_file_name = file_desc+ '-' + str(time_base_2)+'-OCVD.txt'
    ocvd_fn = os.path.join(root_dir,ocvd_file_name)
    
    np.savetxt(ocvd_fn,ocvd_data,delimiter=',')
    np.savetxt(ocvb_fn,ocvb_data,delimiter=',')
    scope1.configure_sweep(1)
    scope2.configure_sweep(1)
 
def CsTPTDoubleTest(scope1,scope2,dg535,dg_rate,light_time,time_delay,root_dir,time_base_1=5E-5,time_base_2=0.002,extract_time=2E-5,file_desc="",sweeps=3): 
    """_
    使用两个示波器分别采集数据

    第一个示波器采集上升沿触发数据(即TRCE)

    第二个示波器采集下降沿触发数据(即ion)
        _

    Args:
        scope1 (_type_): _第一个示波器_
        scope2 (_type_): _第一个示波器_
        dg535 (_type_): _DG535_
        dg_rate (_type_): _DG535_
        light_time (_type_): _DG535_
        time_delay (_type_): _DG535_
        root_dir (_type_): _DG535_
        time_base_1 (_type_, optional): _description_. Defaults to 5E-5.
        time_base_2 (float, optional): _description_. Defaults to 0.002.
        extract_time (_type_, optional): _description_. Defaults to 2E-5.
        file_desc (str, optional): _description_. Defaults to "".
        sweeps (int, optional): _description_. Defaults to 3.
    """
    dg535.set_time_delay(dg_rate, light_time, time_delay, extract_time)
    
    # 配置示波器
    print("OCVD-Trce start ....")
    scope1.configure_sample_mode('RealTime')
    scope1.configure_trigger_source('C1')
    scope1.configure_trigger_slope('C1', 1)
    scope1.time_base(time_base_1, -4 * time_base_1, 10000)
    scope1.configure_sweep(sweeps)
    scope1.clear_sweep()

    scope2.configure_sample_mode('RealTime')
    scope2.configure_trigger_source('C1')
    scope2.configure_trigger_slope('C1', 2)
    scope2.time_base(time_base_2, -4 * time_base_2, 10000)
    scope2.configure_sweep(sweeps)
    scope2.clear_sweep()
    
    time.sleep((sweeps+1) / dg_rate)
    
    trce_data = scope1.get_waveform('C2')
    ion_data = scope2.get_waveform('C2')
    
    trce_file_name = file_desc + '-'+str(time_base_1)+ '-OCVD_trce.txt'
    trce_fn = os.path.join(root_dir,trce_file_name)
    ion_file_name = file_desc + '-'+str(time_base_2)+ '-OCVD_ion.txt'
    ion_fn = os.path.join(root_dir,ion_file_name)
    np.savetxt(trce_fn, trce_data,delimiter=',')
    np.savetxt(ion_fn, ion_data,delimiter=',')
    
    scope1.configure_sweep(1)
    scope2.configure_sweep(1)
 
    time.sleep(1)
    
    
    
     
    
