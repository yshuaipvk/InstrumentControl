from ctypes import *

dll = windll.LoadLibrary(r"D:\ys\驱动及说明\GCI-73 精密电子定时器\定时器USB驱动\CH372DRV 驱动64位\DRIVER\CH375DLL.DLL")


def openDevice(index):
    index = c_uint32(index)
    index = dll.CH375OpenDevice(index)
    return c_int8(index)

def setTimeout(index,writetimeout=2000,readtimeout=2000):
    index = c_uint32(index)
    writetimeout = c_uint32(writetimeout)
    readtimeout = c_uint32(readtimeout)
    index = dll.CH375SetTimeout(index,writetimeout,readtimeout)
    return c_int8(index)


def writeData(index,buffer='?'):
    c_uint32(index)
    #buffer = create_string_buffer()
    buffer = c_char_p(buffer)
    buffer = byref(buffer)
    length = c_uint8(1)
    dll.CH375WriteData(index,buffer,length)


def closeDevice(index):
    index = c_uint32(index)
    dll.CH375CloseDevice(index)

def open_1():
    openDevice(index=0)
    setTimeout(index=0)
    writeData(index=0)
    closeDevice(index=0)

def close_all():
    openDevice(index=0)
    setTimeout(index=0)
    writeData(index=0, buffer=123)
    closeDevice(index=0)

openDevice(index=0)
setTimeout(index=0)
writeData(index=0,buffer=128)
closeDevice(index=0)