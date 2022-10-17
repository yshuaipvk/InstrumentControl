import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from DataProcessing.trce_Ion import *

root_dir = r"C:\Users\SDMM\Desktop\manuscript\Data file\PCBM变温数据-暂未处理"

filenams = os.listdir(root_dir)

trces = []
ions = []
OCVB_1ms= []
OCVBs = []
for fn in filenams:
    if re.findall('trce',fn):
        trces.append(fn)
    elif re.findall('ion',fn):
        ions.append(fn)
    elif re.findall("ocvb",fn):
        if re.findall("0.01s",fn):
            OCVB_1ms.append(fn)
        else:
            OCVBs.append(fn)


# trce

df = pd.DataFrame()
tems = []
max_voltages = []
# for i in range(len(OCVBs)):
#     OCVB = OCVBs[i]
#     root = os.path.join(root_dir,OCVB)
#     tem = OCVB[8:-12]
#     tems.append(tem)
#     data = np.loadtxt(root, delimiter=',')
#     max_voltage = np.max(data[:,1])
#     max_voltages.append(max_voltage)
#
#     if i ==0:
#         df.insert(loc = 0,column="time",value=data[:,0])
#
#     df.insert(loc=i+1,column=tem,value=data[:,1])
# df.insert(loc=0,column='tempurature',value=tems)
# df.insert(loc=1,column='max voltage ',value=max_voltages)
# df.sort_values(by='tempurature',inplace=True)
# # save_data_frame(root_dir,df,'origin_OCVB_data.csv')
# csv_fn = os.path.join(root_dir,"maxvoltage.csv")
# df.to_csv(path_or_buf=csv_fn,index=None)
# print(df)



df = pd.DataFrame()
aeras = []
voltages = []
tems = []
origin_trce_df = pd.DataFrame()
origin_ion_df = pd.DataFrame()
i = 0
j=0
for trc in trces:
    fr = os.path.join(root_dir,trc)
    tem = trc[5:-9]
    data = np.loadtxt(fr,delimiter=',')
    if i==0:
        origin_trce_df.insert(loc=0,column='time',value=data[:,0])
    origin_trce_df.insert(loc=i+1, column=tem, value=data[:, 1])
    aera = integrate_trce(data)
    aeras.append(aera)
    i+=1
    tems.append(tem)

for ion in ions:
    tem = ion[5:-8]
    #tems.append(tem)
    fr = os.path.join(root_dir,ion)
    data = np.loadtxt(fr,delimiter=',')
    if j==0:
        origin_ion_df.insert(loc=0,column='time',value=data[:,0])
    origin_ion_df.insert(loc=j+1, column=tem, value=data[:, 1])
    j+=1
    voltage = get_voltage_recovery(data)
    voltages.append(voltage)

tems.sort()
tems.insert(0,'time')
origin_ion_df = origin_ion_df[tems]
origin_trce_df = origin_trce_df[tems]
save_data_frame(origin_ion_df,root_dir,'origin_ion_data.csv')
save_data_frame(origin_trce_df,root_dir,'origin_trce_data.csv')
