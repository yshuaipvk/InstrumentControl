#电阻箱控制

import pyvisa as visa


class M642():
    def __init__(self):
        address = 'COM3'
        rm = visa.ResourceManager()
        self.resis = rm.open_resource(address)
        self.resis.write('syst:rem')  # syst:rem表示远程控制，syst:loc 表示本地控制

    def write_command(self, command):
        # self.resis.write('syst:rem')
        # time.sleep(0.1)
        self.resis.write(command)
        # time.sleep(0.1)
        # self.resis.write('syst:loc')



    def set_resistance(self, R):  # 设置电阻
        self.resis.write('RES ' + str(R))

    def open(self):
        self.resis.write('OUTP ON')  # 打开

    def close(self):
        self.resis.write('OUTP OFF')  # 关闭
        self.resis.write('syst:loc')  # 切换为本地控制

    def switch_mode(self, mode):  # fast表示在400 us从R1变为R2，400us内电阻不确定；smooth表示在ms内从R1均匀变化到R2
        if mode == 1:
            self.resis.write('outp:swit fast')
        elif mode == 2:
            self.resis.write('outp:swit smooth')

    def configure_short(self, channel='OFF'):
        self.resis.write('OUTP:SHOR' + channel)

