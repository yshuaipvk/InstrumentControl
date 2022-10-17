# ----------------------------------------
# 寻找高斯峰半峰宽
# 输入数据为X，Y1，Y2，Y3...，X从小到大排列，若X从大到小排列则半峰宽为负值
# 返回数据为：温度、左边X值、右边X值、半峰宽、积分面积
# ---------------------------------------
import numpy as np
import pandas as pd
from scipy import integrate
np.set_printoptions(suppress=True)
def find_FWHM(data):
    wavelength_ = data[:, 0]
    data = data[:, 1:]
    FWHMs = []
    temperature = list(range(78,308,10))
    for i in range(data.shape[1]):
        tem = temperature[i]
        x =data[:,0]
        itensity = data[:, i]
        aera = integrate.trapz(x,itensity)
        peak_value = max(itensity)
        half_peak_value = peak_value / 2
        peak_value_index = np.where(peak_value == itensity)
        peak_value_index = peak_value_index[0]
        left_wavelength_index = find_closest_number(half_peak_value, itensity[:peak_value_index[0]])
        right_wavelength_index = find_closest_number(half_peak_value, itensity[peak_value_index[0]:]) + \
                                 peak_value_index[0]
        left_wavelength = wavelength_[left_wavelength_index]
        right_wavelength = wavelength_[right_wavelength_index]
        FWHM_ = right_wavelength - left_wavelength

        result = [tem,left_wavelength, right_wavelength, FWHM_,aera]
        FWHMs.append(result)
    return FWHMs


def find_closest_number(num, waveform):
    b = []
    for i in range(len(waveform)):
        difference_value = abs(waveform[i] - num)
        b.append(difference_value)
    index_2 = np.where(min(b) == b)
    index_2 = index_2[0]
    return index_2[0]

root_dir = r"C:\Users\SDMM\Desktop\4.csv"

df = pd.read_csv(root_dir,delimiter=",")

df = np.array(df)
out =find_FWHM(df)
np.savetxt(r"C:\Users\SDMM\Desktop\4.txt",out,delimiter=',')


