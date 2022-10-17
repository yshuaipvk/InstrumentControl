# 三联光谱仪：stage1 地址COM3，stage2地址 COM4，stage3地址COM5
# 波长设置
# waveleng_1
# wavelength_2 = wavelength_1 + 5.18
# wavelength_3 = - (wavelength_1) + 1.52

import pyvisa as visa




class triVista():
    def __init__(self, address):
        rm = visa.ResourceManager()
        self.stage = rm.open_resource(address)

    def init_place(self, wavelength):
        self.stage.write('{} GOTO'.format(wavelength))

    def move(self, wavelength):
        self.stage.write('{} NM'.format(wavelength))


stage_1 = triVista(address='COM3')
stage_2 = triVista(address='COM4')
stage_3 = triVista(address='COM5')
