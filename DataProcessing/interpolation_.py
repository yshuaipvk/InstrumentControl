# ----------------------------------------------------------------------------------#
# 插值在数据点中增加数值                                                            #
# 输入为为x，y，point，kind，point表示相邻两个点插入点的数目，kind表示方法，默认为2 #
# 返回为x_new，y_new                                                                #
# ----------------------------------------------------------------------------------#
import numpy as np
from scipy.interpolate import interp1d


def interpolation(x, y, point, kind=2):
    if kind == 1:
        f = interp1d(x, y)
    elif kind == 2:
        f = interp1d(x, y, kind='cubic')
    x_new = np.linspace(min(x), max(x), num=point * len(x), endpoint=True)
    y_new = f (x_new)
    return x_new, y_new

