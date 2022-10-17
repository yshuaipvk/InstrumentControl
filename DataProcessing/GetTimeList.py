# -----------------------------------------------------------------------------
# 根据OCVD或者OCVB数据以每25 mv作为间隔获取对应的时间作为电荷抽取的时间
# -----------------------------------------------------------------------------

import numpy as np

def get_time_list(data):
    # 时间轴
    time_values = data[:, 0]
    # 电压轴
    voltage_values = data[:, 1]
    # 获取最大值、最小值
    max_value = np.max(voltage_values)
    min_value = np.min(voltage_values)
    # 获取抽取次数
    r = int((max_value - min_value) / 0.025)
    # 根据OCVD数据以每25mv确定电压间隔，计算对应的衰减时间
    delay_time_index = []
    for i in range(r):
        volt = (r - i) * 0.025
        indx = []
        for j in range(len(voltage_values)):
            if abs(voltage_values[j] - volt) <= 0.001:
                indx.append(j)
        if indx:
            delay_time_index.append(indx[0])
    voltage_value = []
    delay_time_list = []
    for index in delay_time_index:
        delay_time_list.append(time_values[index])
        voltage_value.append(voltage_values[index])
    return delay_time_list

    


