# -----------------------------------------------------
# 工作状态下电荷抽取和离子迁移检测
# 将电池两端接入电阻
# 用调节稳态光是电池能达到Voc
# 改变电阻使电池处于不同工作状态
# -------------------------------------------------------

from Instrument.LecroyScope import HDO4054A
from Instrument.DG535 import DG
import time
import Experiment.experiment_fuction as ef
import numpy as np

scope = HDO4054A()
dg = DG()

ApplyVoltage = '1MOHM'
TimeList = [ 0.001,0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 4, 6, 10,12,14,16,20]

rate = 0.2
# TimeList=[0.001,0.005]
# OCVB
def OCVB():
    dg.init_ins()
    scope.stop()
    scope.clear_sweep()
    scope.configure_sample_mode('RealTime')
    scope.configure_trigger_source('C1')
    scope.time_base(1, -4, 10000)
    scope.configure_trigger_slope(channel='C1', slope=1)
    scope.clear_sweep()
    # scope.configure_sweep(1)
    dg.set_time_delay(rate, 8, 0, 0)
    scope.start()
    time.sleep(1 / rate - 1)
    OCVB_save_root = ef.set_save_root(file_name=ApplyVoltage + '_OCVB')
    OCVB_DATA = scope.get_waveform('C2')
    np.savetxt(OCVB_save_root, OCVB_DATA, delimiter=',')
    print('OCVB done')
    time.sleep(0.5)
    scope.stop()
    # OCVD
    scope.time_base(1, -4, 10000)
    scope.configure_trigger_slope(channel='C1', slope=2)
    scope.clear_sweep()
    scope.start()
    time.sleep(1 / rate)
    OCVD_save_root = ef.set_save_root(file_name=ApplyVoltage + '_OCVD')
    OCVD_DATA = scope.get_waveform('C2')
    np.savetxt(OCVD_save_root, OCVD_DATA, delimiter=',')
    print('OCVD done')


def OcvbTrceIon():
    i = 1
    scope.configure_sweep(2)
    for delay_time in TimeList:
        # OCVB_TRCE
        rate=0.02
        if delay_time>=1:
            rate=0.01
        scope.configure_sample_mode(mode='RealTime')
        scope.configure_trigger_source('C1')
        scope.configure_trigger_slope(channel='C1', slope=1)
        dg.set_time_delay(rate, delay_time, 0, 0.0001)
        scope.time_base(0.0001, -0.0004, 10000)
        scope.start()
        time.sleep(0.01)
        scope.time_base(0.0001, -0.0003, 10000)
        time.sleep(0.01)
        scope.time_base(0.0001, -0.0004, 10000)

        time.sleep(2 / rate - 1)
        TrceDateRoot = ef.set_save_root(file_name=ApplyVoltage + '_OCVB_' + str(delay_time) + '_trce')
        TrceDate = scope.get_waveform('C2')
        np.savetxt(TrceDateRoot, TrceDate, delimiter=',')
        print('OCVB Trce Done')
        time.sleep(1)
        scope.configure_trigger_slope('C1', 2)
        scope.time_base(0.02, -0.08, 10000)
        scope.clear_sweep()
        scope.start()
        time.sleep(2 / rate - 1)
        IonDateRoot = ef.set_save_root(file_name=ApplyVoltage + '_OCVB_' + str(delay_time) + '_ion')
        IonDate = scope.get_waveform('C2')
        np.savetxt(IonDateRoot, IonDate, delimiter=',')
        print('OCVB Ion done')
        print(str(i) + ' of ' + str(len(TimeList)) + ' has done')
        print('---------------------')
        i += 1
        time.sleep(1)


def OcvdTrceIon():
    i = 1
    scope.configure_sweep(2)
    for delay_time in TimeList:
        # OCVB_TRCE
        dg.init_ins()
        scope.configure_sample_mode(mode='RealTime')
        scope.configure_trigger_source('C1')
        scope.time_base(0.0001, -0.0004, 10000)
        scope.configure_trigger_slope(channel='C1', slope=1)
        scope.clear_sweep()
        dg.set_time_delay(rate, 8, delay_time, 0.0001)
        scope.start()
        time.sleep(1 / rate - 1)
        TrceDateRoot = ef.set_save_root(file_name=ApplyVoltage + '_OCVD_' + str(delay_time) + '_trce')
        TrceDate = scope.get_waveform('C2')
        np.savetxt(TrceDateRoot, TrceDate, delimiter=',')
        print('OCVD Trce Done')

        scope.configure_trigger_slope('C1', 2)
        scope.time_base(0.02, -0.08, 10000)
        scope.clear_sweep()
        scope.start()
        time.sleep(1 / rate - 1)
        IonDateRoot = ef.set_save_root(file_name=ApplyVoltage + '_OCVD' + str(delay_time) + '_ion')
        IonDate = scope.get_waveform('C2')
        np.savetxt(IonDateRoot, IonDate, delimiter=',')
        print('OCVD Ion done')
        print(str(i) + ' of ' + str(len(TimeList)) + ' has done')
        print('--------------------------')
        i += 1
def ocvdOnWork():
    scope.configure_trigger_slope(channel='C1', slope=1)
    scope.configure_sweep(2)
    scope.time_base(0.1,-0.4,10000)
    time.sleep(200)
    OCVB_Short_data=scope.get_waveform('C2')
    OCVB_Short_root=ef.set_save_root(file_name=ApplyVoltage + '_OCVB_small')
    np.savetxt(OCVB_Short_root,OCVB_Short_data,delimiter=',')
    scope.clear_sweep()
    scope.time_base(5,-20,10000)
    time.sleep(200)
    OCVB_large_data = scope.get_waveform('C2')
    OCVB_large_root = ef.set_save_root(file_name=ApplyVoltage + '_OCVB_large')
    np.savetxt(OCVB_large_root, OCVB_large_data, delimiter=',')
    scope.clear_sweep()
    scope.configure_trigger_slope('C1',2)
    scope.time_base(0.1,-0.4 , 10000)
    time.sleep(200)
    OCVD_Short_data = scope.get_waveform('C2')
    OCVD_Short_root = ef.set_save_root(file_name=ApplyVoltage + '_OCVD_small')
    np.savetxt(OCVD_Short_root, OCVD_Short_data, delimiter=',')
    scope.clear_sweep()
    scope.time_base(5, -20, 10000)
    time.sleep(200)
    OCVD_large_data = scope.get_waveform('C2')
    OCVD_large_root = ef.set_save_root(file_name=ApplyVoltage + '_OCVD_large')
    np.savetxt(OCVD_large_root, OCVD_large_data, delimiter=',')
ocvdOnWork()