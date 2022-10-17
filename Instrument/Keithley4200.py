import pyvisa as visa
import struct
import time



class Keithley():


    def __init__(self, address='TCPIP0::169.254.101.174::1225::SOCKET'):
        try:
        # address = 'TCPIP0::169.254.164.203::inst0::INSTR'
            rm = visa.ResourceManager()
            self.inst = rm.open_resource(address,open_timeout=10000,read_termination='\00')
            # self.scope.write('CORD HI;CHDR OFF')
            print('Open success')
        except:
            print("Can not finf scope,please check the cable or address")
    
    def write(self,command):
        command = command+'\0'
        self.inst.write(command)
        
    
    def indefy(self):
        self.inst.write('*IDN?\0')
        return self.inst.read()
    def close(self):
        self.inst.close()
    def de(self):
        self.inst.write('DE\0')

    def CVU(self):
    
        # self.write(':CVU:RESET')
        # self.write(':CVU:MODE 1')
        # self.write(':CVU:MODEL 2')
        # self.write(':CVU:SPEED 2')
        # self.write(':CVU:ACZ:RANGE 0')
        # self.write(':CVU:FREQ 1E6')
        # self.write(':CVU:SWEEP:DCV -1, -1, -0.2')
        # self.write(':CVU:SWEEP:DCV')
        # self.write(':CVU:TEST:RUN')
        self.write(':DR1')
        self.write(':CVU:RESET')
        self.write(":CVU:MODE 1")
        self.write("MODEL 1")
        self.write(':CVU:SPEED 2')
        self.write(':CVU:FREQ 1E6')
        self.write(':CVU:SWEEP:DCV 0,1,-0.2')
        self.write(':CVU:DELAY:SWEEP 1')
        self.write(":CVU:TEST:RUN")
        # self.inst.assert_trigger()
        
        self.inst.wait_for_srq()
        return self.inst.query(':CVU:DATA:Z?')

    def DLCP(self,Vmax,start,stop,step,freq):
        self.write("UL")
        self.write("EX DLCP")
    # def GD(self):
    #     self.write('UL')
    #     self.write('GD DLCP ACSweep')
    #     return self.inst.read_bytes(128)
keith = Keithley()
# b = keith.indefy()
# print(b)  
b = keith.CVU()
print(b)



# echo_commands = 0
# def instrument_write(instrument_object, my_command):
#     if echo_commands == 1:
#         print(my_command)
#     instrument_object.write(my_command)
#     return

# def instrument_connect(resource_mgr, instrument_object, instrument_resource_string, timeout, do_id_query, do_reset, do_clear): 
#     instrument_object = resource_mgr.open_resource(instrument_resource_string)
#     if do_id_query == 1:
#         print(instrument_query(instrument_object, "*IDN?"))
#     if do_reset == 1:
#         instrument_write(instrument_object, "*RST")
#     if do_clear == 1:
#         instrument_object.clear()
#     instrument_object.timeout = timeout
#     return resource_mgr, instrument_object

# def instrument_query(instrument_object, my_command):
#     if echo_commands == 1:
#         print(my_command)
#     return instrument_object.query(my_command)




# def instrument_read(instrument_object):
#     return instrument_object.read()



# def instrument_disconnect(instrument_object):
#     instrument_object.close()
#     return


# instrument_resource_string = "TCPIP0::169.254.101.174::1225::SOCKET"
# term_char = ''  # This was set in KCON, should be '' for ethernet, character = NONE
# resource_manager = visa.ResourceManager()  # Opens the resource manager
# inst = None
# resource_manager, inst = instrument_connect(resource_manager, inst, instrument_resource_string, 5000, term_char, 1, 1)
# instrument_query(inst, "DE")
# instrument_query(inst, "CH1, 'VS', 'IS', 1, 3")
# instrument_query(inst, "CH2, 'VD', 'ID', 1, 1")
# instrument_query(inst, "CH3, 'VG', 'IG', 1, 2")
# instrument_query(inst, "SS")
# instrument_query(inst, "VR1, 0, 5, 0.1, 100e-3")
# instrument_query(inst, "VP2, 1, 4, 100e-3")
# instrument_query(inst, "VC1, 0, 100e-3")
# instrument_query(inst, "HT 0")
# instrument_query(inst, "DT 0.001")
# instrument_query(inst, "IT2")
# instrument_query(inst, "RS 5")
# instrument_query(inst, "RG 1, 100e-9")
# instrument_query(inst, "RG 2, 100e-9")
# instrument_query(inst, "RG 3, 100e-9")
# instrument_query(inst, "SM")
# instrument_query(inst, "DM1")
# instrument_query(inst, "XN 'VD', 1, 0, 5")
# instrument_query(inst, "YA 'ID', 1, 0, 0.04")
# instrument_query(inst, "MD")
# instrument_query(inst, "ME1")
# # Wait for measurement to complete

# status = instrument_query(inst, "SP")
# while int(status) != 1:
#     status = instrument_query(inst, "SP")
#     time.sleep(1)
# instrument_disconnect(inst)
# resource_manager.close

