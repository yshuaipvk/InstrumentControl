#找到电压回复的最大值


import os
import numpy as np
import re

rootdir = 'D:\\ys\\DATA\\Dynamic\\20190509'
file_name_list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
b = np.empty(shape=[0, 3], dtype=str)
b = np.append(b, [['filename', 'voltage', 'rollback']], axis=0)
for i in range(len(file_name_list)):
    file_name = file_name_list[i]
    path = os.path.join(rootdir, file_name_list[i])
    # 找到txt文件
    if os.path.isfile(path) and re.search('.txt', path):
        # 载入数据
        data = np.loadtxt(path, skiprows=5, delimiter=',')
        x_value = data[:, 0]  # x值
        y_value = data[:, 1]  # y值
        x_ = []
        x__ = []
        for i in range(len(x_value)):
            # 截取时间小于0部分，电压上升部分
            if x_value[i] < 0:
                x_.append(i)
        x_rise = x_value[:x_[-1]]  # 索引 -1即开始抽取时间
        y_rise = y_value[:x_[-1]]
        voltage = max(y_rise)  # 开始抽取时电压

        y_delay = y_value[x_[-1] + 1:]  # 截取抽取完成之后部分
        voltage_rollback = max(y_delay)  # 获取回复电压
        # out_put.append(file_name)  #文件名
        list_ = [file_name, str(voltage), str(voltage_rollback)]
        a = np.array([list_])
        b = np.append(b, a, axis=0)
output_file_addr = rootdir + '\\output.csv'
np.savetxt(output_file_addr, b, fmt='%s', delimiter=',')
