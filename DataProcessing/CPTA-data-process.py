import numpy as np
import matplotlib.pyplot as plt
import re
import os
import pandas as pd
root = r'D:\ys\OCVB\20211002-Control-OCVB-TRCE'

file_names = os.listdir(root)

ion_100us = []
ion_10ms =[]
ion_1ms =[]
for fn in file_names:
    #fn_dir = os.path.join(root,fn)
    if re.findall('OCVD_ion.txt',fn):
        _fn = fn[4:-12]
        _fn =_fn[-6:]
        if re.findall("0.0001",_fn):
            ion_100us.append(fn)
        elif re.findall("0.001",_fn):
            ion_1ms.append(fn)
        elif re.findall("0.01",_fn):
            ion_10ms.append(fn)
print(ion_10ms)
ion_df = pd.DataFrame()
extract_times =[]
Vrs = []
for ion_fn in ion_10ms:
    fn_dir = os.path.join(root,ion_fn)
    extract_time = float(ion_fn[7:-16])
    extract_times.append(extract_time)
    data = np.loadtxt(fn_dir,delimiter=',')
    x =data[:,0]
    y = data[:,1]
    Vr = max(y[1050:])
    Vrs.append(Vr)

ion_df.insert(loc=0,column='Extract time',value = extract_times)
ion_df.insert(loc=1,column='Voltage recovery',value=Vrs)
ion_df.sort_values(by='Extract time',inplace=True)

out_file = "Li_out.csv"
out_dir = os.path.join(root,out_file)
ion_df.to_csv(out_dir,index=None)