#仪器DG535的控制


import pyvisa as visa

class DG():
    def __init__(self,address='GPIB0::15::INSTR'):
        try:
            rm = visa.ResourceManager()
            self.dg535 = rm.open_resource(address)
        except:
            print('can not find DG535, please check the cable or address')

    # init DG535;set trigger moder inter
    def init_ins(self):
        self.dg535.write('CL')
        self.dg535.write('TM 0')

    def trigger_rate(self, rate):
        self.dg535.write('TR 0,' + str(rate))

    def A_T(self, delay):
        self.dg535.write('DT 2,1,' + str(delay))

    def B_A(self, delay):
        self.dg535.write('DT 3,2,' + str(delay))

    def C_B(self, delay):
        self.dg535.write('DT 5,3,' + str(delay))

    def D_C(self, delay):
        self.dg535.write('DT 6,5,' + str(delay))

    def set_time_delay(self, rate, b, c, d):
        self.dg535.write('TM 0')
        self.trigger_rate(rate)
        self.B_A(b)
        self.C_B(c)
        self.D_C(d)

    def visa_close(self):
        self.dg535.close()


