#!/usr/bin/env python
# coding: utf-8
"""
处理TRCE和Ion数据，积分电量，最大回复电压，抽取时间及对应的抽取电压
"""

import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt
from  scipy import integrate
import os 
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 文件路径
# root_dir = r"C:\Users\SDMM\Desktop\20200908"
# file_names = os.listdir(root_dir)

# 从文件名称获取抽取时间




def get_extract_voltage_in_trce(data):
    """
    :param data:
    :return:
    """
    mask_1 = (data[:,0]>=0)
    mask_2 = (data[:,0]<0)
    x_1 = data[mask_1,0]
    x_2 = data[mask_2,0]
    y_1 = data[mask_1, 1]
    y_2 = data[mask_2, 1]
    if np.abs(x_1[0])<np.abs(x_2[-1]):
        extract_voltage = y_1[0]
    else:
        extract_voltage = y_2[-1]

    return extract_voltage

def file_classification(filenames,first_keywords,second_keywords):
    """
    :param filenames: a list,target filename to classification
    :param first_keywords: the first class standard
    :param second_keywords: the second class standard
    :return: df , a
    """
    df = pd.DataFrame()
    for first_keyword in first_keywords:
        for second_keyword in second_keywords:
            column = first_keyword + "-" + second_keyword
            df.insert(loc=0, column=column, value=None)
    i=0
    for file_name in filenames:
        for first_keyword in first_keywords:
            for second_keyword in second_keywords:
                column = first_keyword + "-" + second_keyword
                if re.findall(first_keyword,file_name) and re.findall(second_keyword,file_name):
                    df.loc[i,column]=file_name
        i+=1
    return df

def loaddata(filename,rootdir,delimiter=','):
    """load data from a file path
    :param filename
    :param rootdir:
    :param delimiter:
    :return: _data:
    """
    filedir = os.path.join(rootdir,filename)
    file_data = pd.read_csv(filedir,delimiter=delimiter)

    _data = np.array(file_data)
    return _data

def integrate_trce(trce_data):
    """intergrate trce data
    :param trce_data
    :return: aera
    """
    mask = (trce_data[:,0]>0)
    x= trce_data[mask,0]
    y = trce_data[mask,1]
    x = x[0:50]
    y = y[0:50]
    aera  = integrate.trapz(y=y,x=x)

    return aera/25

def save_data_frame(df,root,filename):
    path = os.path.join(root,filename)
    df.to_csv(path,index=None)

def get_voltage_recovery(ion_data):
    """get the max voltage recovery in ion data
    :param ion_data:
    :return:
    """
    mask = (ion_data[:,0]>=0)
    y = ion_data[mask,1]
    _voltage_recovery = np.max(y)

    return _voltage_recovery


class dataProcess:
    '''
    用于处理TRCE-Ion的数据
    实现方案如下
    1.列出文件-文件分类(trce or ion)
    2.trce()
        2.1 根据文件名称获取抽取时间，并按照抽取时间对文件名进行排序，
        2.2 根据排序之后的文件列表进行文件处理
        2.3 进行积分获取电荷量(Aera)
        2.4 获取抽取时刻电压(Vmax)
        2.5 将trce数据提取到一个dfData中(trce数据进行切片，只需要抽取部分)
    3.ion()
        3.1 根据文件名称获取抽取时间，并按照抽取时间对文件名进行排序
        3.2 根据排序之后的文件列表进行文件处理
        3.3 提取出电压回复最大值(Vr)
        3.4 对电压回复上升沿部分进行单只数拟合，得到y0，A，t，其中t为上升沿寿命
        3.5 将ion数据提取到一个dfData中

    4.SaveData()
        4.1.在一个df中依次插入 抽取时间、抽取电压、积分面积、电压回复最大值，拟合参数，并保存到csv文件
        4.2 分别保存trce和ion原始数据文件


    '''
    def __init__(self,root_dir,flag="OCVD"):
        self.root_dir = root_dir
        self.flag = flag
        self.fileName = os.listdir(root_dir)
        self.ocvdFiles,self.trceFiles,self.ionFiles = self.fileIden()

    
    def fileIden(self):
        # 根据文件名称归档文件
        # if self.flag =='OCVD':
        OCVD_files = []
        trce_files = []
        ion_files = []
        for file_name in self.fileName:
            if re.findall(self.flag+'.txt',file_name,):
                    OCVD_files.append(file_name)
            elif re.findall('ion.txt',file_name,):
                ion_files.append(file_name)
            elif re.findall('trce.txt',file_name,):
                trce_files.append(file_name)  
        return OCVD_files,trce_files,ion_files

    def get_time_stamps_in_filname(self,filenames,num):
            """ get extract time from filename
            :param filenames: a list of filenames
            :return: time_stamps: a float list make up of all extract time
            """
            # 有点问题
            pass
            # time_stamps =[]
            # for filename in filenames:
            #     time_stamp = filename[:-1*num]
            #     time_stamps.append(time_stamp)
                # try:
                #     time_stamp = re.findall(r'\d+\.?\d*e?[-+]?\d+',filename)
                #     time_stamp = float(time_stamp[0])
                #     time_stamps.append(time_stamp)
                # except:
                #     time_stamp = re.findall(r'\d+', filename)
                #     time_stamp = float(time_stamp[0])
                #     time_stamps.append(time_stamp)
            # return time_stamps

             
    def trce(self):
        # 处理TRCE数据
        
        # 1.获取抽取时间，进行排序
        df = pd.DataFrame()
        df.insert(loc=0,value=self.trceFiles,column='TRCE File')
        timeStamps = []
        for i in range(len(self.trceFiles)):
            trceFile = self.trceFiles[i]
            timeStamp = float(trceFile[:-20])
            timeStamps.append(timeStamp)
        df.insert(loc=1,value=timeStamps,column='Extract Time')
        df.sort_values(by='Extract Time',inplace=True)
        # 2.利用排序之后的文件进行处理
        dataDf = pd.DataFrame()
        aeras = []
        Vmax = []
        TF = list(df['TRCE File'])
        TS = list(df['Extract Time'])
        for i in range(len(TF)):
            trceFile = TF[i]
            ts = TS[i]
            fileDir = os.path.join(self.root_dir,trceFile)
            data = np.loadtxt(fileDir,delimiter=',')
            # data = np.delete(data,[1002],axis=0)  # 删除第1003个跳点
            x = data[900:1400,0]
            y = data[900:1400,1]
            if i ==0:
                dataDf.insert(loc=0,value=x,column='Time')
            dataDf.insert(loc=i+1,value=y,column=ts)  # 保存原始数据

            mask = (x>0)
            x= x[mask]
            y = y[mask]
            x = x[0:50]
            y = y[0:50]
            aera  = integrate.trapz(y=y,x=x)  # 积分获取面积
            aeras.append(aera) 
            Vmax.append(np.max(y))   # 抽取时的电压，即y的最大值

        return TS,aeras,Vmax,dataDf


    def ion(self):
        # 处理电压回复数据
        # 1.排序
        df = pd.DataFrame()
        taves = []
        df.insert(loc=0,value=self.ionFiles,column='Ion File')
        timeStamps = []
        for i in range(len(self.ionFiles)):
            ionFile = self.ionFiles[i]
            timeStamp = float(ionFile[:-18])
            timeStamps.append(timeStamp)
        df.insert(loc=1,value=timeStamps,column='Extract Time')
        df.sort_values(by='Extract Time',inplace=True)

        dataDf = pd.DataFrame()
        Vrs = []
        Fitted = []
        TF = list(df['Ion File'])
        TS = list(df['Extract Time'])
        # 2.根据排序之后的文件进行处理
        for i in range(len(TF)):
            ionFile = TF[i]
            et = TS[i]
            fileDir = os.path.join(self.root_dir,ionFile)
            data = np.loadtxt(fileDir,delimiter=',')
            x = data[900:5000,0]
            y = data[900:5000,1]
            if i ==0:
                dataDf.insert(loc=0,value=x,column='Time')
            dataDf.insert(loc=i+1,value=y,column=et)   # 保存原始数据

            mask = (x>0)
            x = x[mask]
            y = y[mask]
            # 电压回复最大值(排序之后去前20个最大值进行平均)
            y.sort()
            # vr = np.average(y[-20:])
            vr= np.max(y)  
            Vrs.append(vr)
            
            # 获取电压回复上升沿部分
            index = np.where(y==vr)
            index =index[0][0]
            fit_x = x[:index]
            fit_y = y[:index]

            def f(x,y0,A1,t1,A2,t2):
                return y0 + A1 * np.exp(-x/t1) +A2 * np.exp(-x/t2)
            # 估计初始值
            p0 =[y[index],-0.2,x[int(index*0.3)],-0.3,x[int(index*0.1)]]
            # 拟合
            popt,poc = curve_fit(f,fit_x,fit_y,p0=p0)
            tave =(popt[1]*popt[2]+ popt[3]*popt[4])/(popt[1]+popt[3])
            # Fitted.append(popt)
            taves.append(tave)

        taves = np.array(taves)
        Vrs = np.array(Vrs)
        return Vrs,taves,dataDf

    def saveData(self):
        extractTime,aeras,Vmax,trceDf = self.trce()
        Vrs,taves,ionDf = self.ion()
        df = pd.DataFrame()
        trceDf.to_csv(os.path.join(self.root_dir,'trce_out.csv'),index=None)
        ionDf.to_csv(os.path.join(self.root_dir,'ion_out.csv'),index=None)
        df = pd.DataFrame()
        df.insert(loc=0,value=extractTime,column='Extract Time')
        df.insert(loc=1,value=Vmax,column='Extract Voltage')
        df.insert(loc=2,value=aeras,column='Aeras')
        df.insert(loc=3,value=Vrs,column='Voltage Recovery')
        df.insert(loc=4,value=taves,column='t')
        # df.insert(loc=5,value=fitted[:,1],column='A')
        # df.insert(loc=6,value=fitted[:,2],column='t')
        df.to_csv(os.path.join(self.root_dir,'out_come.csv'),index=None)

# import matplotlib.pyplot as plt 
# root_dir = r'D:\ys\DATA\trce-total\CPTA-OCVD-trce'

# DP = dataProcess(root_dir=root_dir,flag='OCVD')
# DP.saveData()


class TemDataProcess:

    def __init__(self,root_dir) -> None:
    
        self.root_dir = root_dir
        self.fileName = os.listdir(root_dir)
        self.trceFiles,self.ionFiles,self.tems = self.fileIden()
        

    def fileIden(self):
        trceFile = []
        ionFiles = []
        tems = []
        for file in self.fileName:
            if re.findall('trce.txt',file):
                trceFile.append(file)
                tem = file[:3]
                tems.append(tem)
            elif re.findall('ion.txt',file):
                ionFiles.append(file)

        return trceFile,ionFiles,tems

    def trce(self):
        trceDf = pd.DataFrame()
        
        for i in range(len(self.trceFiles)):
            trceFile =  self.trceFiles[i]
            fileDir = os.path.join(self.root_dir,trceFile)
            data = np.loadtxt(fileDir,delimiter=',')
            x = data[900:3000,0]
            y = data[900:3000,1]

            if i == 0:
                trceDf.insert(value=x,loc=0,column = 'Time')
            trceDf.insert(value=y,loc=i+1,column=trceFile)
        
        return trceDf

    def ion(self):
        ionDf = pd.DataFrame()
        vrs= []
        # Fitted = []
        taves = []
        for i in range(len(self.ionFiles)):
            ionFile =  self.ionFiles[i]
            fileDir = os.path.join(self.root_dir,ionFile)
            data = np.loadtxt(fileDir,delimiter=',')
            x = data[900:4000,0]
            y = data[900:4000,1]
            y_min = np.min(y)
            y_max = np.max(y)
            y = (y-y_min)/y_max
            if i == 0:
                ionDf.insert(value=x,loc=0,column = 'Time')

            ionDf.insert(value=y,loc=i+1,column=ionFile)

            mask = (x>0)
            x = x[mask]
            y = y[mask]
            vr = np.max(y)
            vrs.append(vr)

            index = np.where(y==vr)
            index =index[0][0]
            fit_x = x[:index]
            fit_y = y[:index]
            # 构造单只数方程
            def f(x,y0,A1,t1,A2,t2):
                return y0 + A1 * np.exp(-x/t1) +A2 * np.exp(-x/t2)
            # 估计初始值
            p0 =[y[index],-0.2,x[int(index*0.3)],-0.3,x[int(index*0.7)]]
            # 拟合
            popt,poc = curve_fit(f,fit_x,fit_y,p0=p0)
            tave =(popt[1]*popt[2]+popt[3]*popt[4])/(popt[1]*popt[3])
            # Fitted.append(popt)
            taves.append(tave)
        # Fitted = np.array(Fitted)
        taves = np.array(taves)
        vrs = np.array(vrs)
        return ionDf,vrs,tave
    
    def saveData(self):

        df = pd.DataFrame()
        trceDf = self.trce()
        ionDf,vrs,tave = self.ion()
        trceDf.to_csv(os.path.join(self.root_dir,'trce.csv'),index=None)
        ionDf.to_csv(os.path.join(self.root_dir,'ion.csv'),index=None)
        df.insert(loc=0,value=self.tems,column='Tems')
        df.insert(loc=1,value=vrs,column="Vr max")
        df.insert(loc=2,value=tave,column='tave')
        # df.insert(loc=3,value=fitted[:,1],column='A')
        # df.insert(loc=4,value=fitted[:,2],column='t')
        df.to_csv(os.path.join(self.root_dir,'out.csv'),index=None)
        

# TDP = TemDataProcess(root_dir=r'D:\ys\DATA\trce-total\CPTA-TEM')
# TDP.saveData()

dp = dataProcess(root_dir=r"D:\ys\OCVB\20211002-Control-OCVB-TRCE",flag='OCVB')

dp.saveData()

            

