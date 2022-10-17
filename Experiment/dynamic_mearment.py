#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# OCVD/OCVB中TRCE、Ion测试
# DG535 A口接示波器C1，用于OCVD/OCVB触发，DG535 C口接示波器C3，用于TRCE/Ion触发
#
#
# -----------------------------------------------------------------------
from Experiment import experiment_fuction as ef
from Instrument.DG535 import DG
from Instrument.LecroyScope import HDO4054A
from DataProcessing.GetTimeList import get_time_list
import time
import numpy as np


def ocvd_or_ocvb_mear(scope, dg, ef, exper='OCVB', rootdir="D:\\Waveforms", rate=0.05):  # 选择测试OCVD或者OCVB  默认为OCVD
    # 初始化
    scope.stop()
    dg.init_ins()
    scope.clear_sweep()
    scope.configure_sample_mode('RealTime')  # 实时采样
    scope.configure_sweep(5)
    scope.time_base(1, -4, 10000)
    # 激活并设置触发为C3，根据实验设置触发斜率
    ef.set_trigger_slope(scope, channel='C3', exper=exper)
    ef.set_delay(dg, rate, 0, 6, 0)
    scope.start()
    save_root = ef.set_save_root(rootdir, exper)
    wait_time = 5 / rate - 1
    time.sleep(wait_time)
    data = scope.get_waveform('C2')
    data = np.array(data)
    np.savetxt(save_root, data, delimiter=',')
    scope.clear_sweep()
    scope.stop()
    time.sleep(2)  # 等待2s，待仪器保存数据
    return data
    #


def trce_or_iron_mear(scope, dg, ef, exper='OCVD', rootdir='D:\\Waveform', delay_time_list=[], rate=0.02,
                      extract_time=0.00002):
    # 初始化DG535
    dg.init_ins()
    scope.stop()
    # 设置示波器为采样方式为 实时
    scope.configure_sample_mode(mode='RealTime')
    scope.activate_channel('C3')  # 开启C3
    scope.deactivate_channel('C1')  # 关闭C1
    # 改变A升B降时间（即光照时间）
    wait_time = 5 / rate - 10
    print('start mearment...')
    for i in range(len(delay_time_list)):
        # TRCE实验
        delay_time = delay_time_list[i]
        # 设置示波器时间轴，对TRCE数据 设置为 200 us/格
        scope.time_base(0.0002, tdl=-0.0008, point=10000)
        scope.configure_sweep(5)  # 设置sweep为5
        scope.configure_trigger_slope('C3', '1')  # 设置触发斜率，1为上升沿触发，2为下降沿触发
        # 在触发线接在DG535的C接口，上升沿触发即开始电荷抽取时间
        scope.start()  # 示波器打开 触发模式为 NORMAL
        # 设置DG535频率 0.02Hz 周期为 50 s

        if exper == 'OCVB':
            ef.set_delay(dg, rate, delay_time, 0, extract_time)
            # C升D降为抽取时间，设置为20 us
        elif exper == 'OCVD':
            ef.set_delay(dg, rate, 6, delay_time, extract_time)
        time.sleep(wait_time)  # 每个周期为50s 等待290s,即5.8个周期，示波器显示数据为在最后0.8个周期已经采集完成，
        # 所以为6个周期，即6个sweep 保存的数据为后5个sweep
        filename_1 = exper + '-Trce-' + str(delay_time)  # 保存文件名
        save_root_1 = ef.set_save_root(rootdir, filename_1)

        data_1 = scope.get_waveform('C2')
        np.savetxt(save_root_1, data_1, delimiter=',')
        time.sleep(2)  # 等待数据保存
        # 清除sweep 初始化DG535，为下一个实验做准备
        scope.clear_sweep()
        scope.stop()
        dg.init_ins()
        print('TECE done')
        time.sleep(2)
        # 离子迁移测量

        # 设置时间，离子迁移为100 ms/格 采样点 10 K
        scope.time_base(0.1, tdl=-0.4, point=10000)
        # 设置触发斜率 2位下降沿触发，即抽取完成后为时间0点
        scope.configure_sweep(5)
        scope.configure_trigger_slope('C1', 2)
        scope.start()  # 打开示波器
        dg.trigger_rate(rate=rate)  # 设置DG535频率 0.02Hz 周期为 50 s
        if exper == 'OCVB':
            ef.set_delay(dg, rate, delay_time, 0, extract_time)
            # C升D降为抽取时间，设置为20 us
        elif exper == 'OCVD':
            ef.set_delay(dg, rate, 6, delay_time, extract_time)
        time.sleep(wait_time)  # 同上
        filename_2 = exper + '-Iron-' + str(delay_time)  # 保存文件名
        save_root_2 = ef.set_save_root(rootdir, filename_2)
        data_2 = scope.get_waveform('C2')
        data_2 = np.array(data_2)
        np.savetxt(save_root_2, data_2, delimiter=',')
        time.sleep(2)
        # 清除sweep，初始化DG535，为一下个延时做准备
        scope.clear_sweep()
        scope.stop()
        dg.init_ins()
        print('ion done')
        print(str(i + 1) + '/' + str(len(time_list)) + ' done')
    print('meearment done')


if __name__ == '__main__':
    experiment = 'OCVD'
    rate = 0.05
    dg = DG()
    scope = HDO4054A()
    OCVD_data = ocvd_or_ocvb_mear(scope, dg, ef, exper=experiment, rate=rate)
    time_list = get_time_list(OCVD_data)
    trce_or_iron_mear(scope, dg, ef, exper=experiment, delay_time_list=time_list, rate=rate)
