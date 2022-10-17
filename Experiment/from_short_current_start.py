# --------------------------------------------------------------------------------------#
# 从短路开始抽取；
# 切换开关至短路状态，然后开始光照，光照结束时切换至开路状态
# 实验变量：改变光照时间
# 仪器DG535、示波器、模拟开关
# A升B降接入激光器和开关，B接入示波器C1作为触发
# 在A时刻开始光照并且开关处于短路状态，在B时刻结束光照，开关切换为开路状态，并记录数据
# -------------------------------------------------------------------------------

import time
from Instrument.LecroyScope import HDO4054A
from Instrument.DG535 import DG
from Instrument.switch import Switch
import Experiment.experiment_fuction as ef
import numpy as np
import os

#
# RATE  = 0.2
# EXTRACT_TIME = 0.000005
#
# DG535 = DG()
# SCOPE = HDO4054A()
# SW = Switch()


def dark_short(scope,dg535,rate,short_time,time_base,save_root):
    """
    dark and short before turn to open circle
    A up B down connect to CMOS switch
    A connect to C1 and set to negative slope trigger
    :param scope:
    :param dg535:
    :param short_time:
    :param rate
    :param time_base
    :param save_root
    :return:
    """
    scope.configure_sample_mode()
    scope.time_base(time_base,-4*time_base,point=10000)
    scope.configure_sweep(3)
    scope.clear_sweep()
    dg535.set_time_delay(rate=rate,b=short_time,c=0,d=0)
    time.sleep(4/rate)
    data = scope.get_waveform('C2')
    fn = 'dark-short-{}.txt'.format(short_time)
    fndir = os.path.join(save_root,fn)
    np.savetxt(fndir,data,delimiter=',')


def light_short(scope,dg535,rate,short_time,time_base,save_root):
    """
    light short before turn to open
    A up B down connected to CMOS and led laser
    change light on time
    :param scope:
    :param dg535:
    :param rate:
    :param short_time:
    :param time_base:
    :param save_root:
    :return:
    """
    print("Change time to {}".format(short_time))
    scope.configure_sample_mode()
    scope.time_base(time_base, -4 * time_base, point=10000)
    scope.configure_sweep(3)
    scope.clear_sweep()
    dg535.set_time_delay(rate=rate, b=short_time, c=0, d=0)
    time.sleep(4 / rate)
    data = scope.get_waveform('C2')
    fn = 'light-short-{}.txt'.format(short_time)
    fndir = os.path.join(save_root, fn)
    np.savetxt(fndir, data, delimiter=',')


def main():
    DG535 = DG()  # DG4535
    SCOPE = HDO4054A()  # 示波器
    sw = Switch('COM10')  # 继电器开关

    # 获取当前日期
    data = ef.get_data()

    # 设置实验超参数
    RATE = 0.025  # 实验频率
    # LIGHT_TIME = 15  # 光照时间
    # EXTRACT_TIME = 0.00004  # 抽取时间
    ROOT_DIR = "D:\\Waveform\\short\\" + data  # 保存路径  以日期为文件夹

    # 创建 文件夹
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)

    # 样品描述
    #file_desc = "OCVB"
    #file_describe = file_desc

    # 时间列表，光照时间（OCVB），衰减时间（OCVD）
    # time_delay_list = [
    #                    5,6,7,8]
    # sw.openChannels(1,2)
    # for light_on in time_delay_list:
    #     light_short(SCOPE,DG535,RATE,light_on,1,ROOT_DIR)


if __name__ == '__main__':
    main()