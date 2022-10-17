#仪器Keithley2400d的控制

from serial import Serial
import time
import pyvisa as visa


class Keithley_2400():
    def __init__(self, address='GPIB0::8::INSTR'):
        try:
        # address='GPIB0::8::INSTR'
        # address='COM5'
            self.rm = Serial(address,9600)
        except:
            print("Can not find Keithley 2400 source meter,please check the cable or address")

    def write_command(self,command):
        command =command+';\r\n'
        command.encode()
        self.rm.write(command)
    def initialize(self):
        #OK
        self.rm.write('*RST;\r\n'.encode())
        self.rm.write(":SENS:FUNC:CONC OFF;\r\n".encode())
        self.rm.write(":SOUR:FUNC VOLT;\r\n".encode())  # volt source
        self.rm.write(":SENS:FUNC 'CURR:DC';\r\n ".encode())
    def sweep_mode(self):
        self.rm.write(':SOURce:VOLTage:MODE SWEep;\r\n'.encode())
        self.rm.write(":SOUR:SWE:RANG AUTO ;\r\n".encode())
    def CurrCompliance(self):
        self.rm.write(':SENS:CURR:PROT 0.1;\r\n'.encode())
        
    def set_range(self, startvolt, stopvolt, step):
        #OK
        start = ":SOUR:VOLT:STAR "+str(startvolt)+" ;\r\n"
        self.rm.write(start.encode())
        stop = ":SOUR:VOLT:STOP "+str(stopvolt)+';\r\n'
        self.rm.write(stop.encode())
        ste = ":SOUR:VOLT:STEP "+str(step)+';\r\n'
        self.rm.write(ste.encode())
        count = (stopvolt-startvolt)/step+1
        count_C = ":TRIG:COUN "+str(count)+" ;\r\n"
        self.rm.write(count_C.encode())
    def set_delay(self,delay):
        delay_C = ":SOUR:DEL "+str(delay)+ " ;\r\n"
        self.rm.write(delay_C.encode())


    def sweep_up_direction(self):
        self.rm.write(":SOUR:SWE:SPAC LIN ;\r\n".encode())
        self.rm.write(":SOUR:SWE:DIR UP ;\r\n".encode())

    def sweep_down_direction(self):
        self.rm.write(":SOUR:SWE:SPAC LIN ;\r\n".encode())
        self.rm.write(":SOUR:SWE:DIR DOWN ;\r\n".encode())  # ？

    def list_measurement(self, volt):
        command = "SOUR:LIST:VOLT " + str(volt)
        self.rm.write('command')
        print(command)
        # self.write("SOUR:LIST:VOLT")

    def start_measurement(self):
        self.rm.write(":OUTP ON;\r\n".encode())
        #self.rm.query(":READ? ;\r\n".encode())

    def gain_data(self):
        results = self.rm.read_until(":FETC?".encode())
        self.rm.write(":OUTP OFF".encode())
        self.rm.write(":SOUR:VOLT 0".encode())
        return results

    def stop(self):
        self.rm.write(':OUTP OFF;\r\n'.encode())

    def set_source_Volt(self):
        command = 'SOUR:FUNC VOLT ;\r\n'.encode()
        self.rm.write(command)

    def set_measure(self):
        self.rm.write(":SENS:FUNC 'CURR:DC' ;\r\n".encode())

    def set_volt(self, volt):
        command = ":SOUR:VOlT "+str(volt)+' ;\r\n'
        self.rm.write(command.encode())

    def cusM(self):
        self.rm.write("*RST ;\r\n".encode())
        self.rm.write(":SENS:FUNC:CONC OFF ;\r\n".encode())
        self.rm.write(":SOUR:FUNC VOLT ;\r\n".encode())
        self.rm.write(""":SENS:FUNC 'CURR:DC' ;\r\n""".encode())
        self.rm.write(":SENS:CURR:PROT 0.1 ;\r\n".encode())
        self.rm.write(":SOUR:VOLT:MODE LIST ;\r\n".encode())
        self.rm.write(":SOUR:LIST:VOLT 7,1,3,8,2 ;\r\n".encode())
        self.rm.write(":TRIG:COUN 5 ;\r\n".encode())
        self.rm.write(":SOUR:DEL 1 ;\r\n".encode())
        self.rm.write(":OUTP ON ;\r\n".encode())
        self.rm.write(":READ? ;\r\n".encode())

rm = Keithley_2400(address='COM9')

rm.cusM()
a = rm.gain_data()
print(a)
# rm.initialize()
# rm.set_range(-0.3,1.3,0.1)
#
# rm.sweep_mode()
# rm.CurrCompliance()
# rm.sweep_up_direction()
# rm.set_delay(0.1)
# rm.start_measurement()
#
# rm.write(':SOUR:VOlT 0.1\n'.encode())
# rm.write(':OUTP ON\n'.encode())
# rm.write(':OUTP OFF\n'.encode())
# rm.write(":SENS:FUNC 'CURR:DC'".encode())