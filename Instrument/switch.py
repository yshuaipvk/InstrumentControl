from serial import Serial
import time


class Switch:

    def __init__(self,address='COM12'):
        self.sw = Serial(address,9600)


    def open(self,cd1,cd2):
        command = "A0"+cd1+'01'+cd2
        command=bytes.fromhex(command)
        self.sw.write(command)


    def close(self,cd1,cd2):
        command = "A0" + cd1 + '00' + cd2
        command = bytes.fromhex(command)
        self.sw.write(command)

    def openChannel(self,channel):
        cd1 = '0'+str(channel)
        cd2 = 'A'+str(channel+1)
        self.open(cd1=cd1,cd2=cd2)

    def closeChannel(self,channel):
        cd1 = '0'+ str(channel)
        cd2 = 'A' + str(channel)
        self.close(cd1,cd2)

    def openChannels(self,*channels):
        self.closeAll()
        for channel in  channels:
            cd1 = '0' + str(channel)
            cd2 = 'A' + str(channel + 1)
            self.open(cd1=cd1, cd2=cd2)

    def closeChannels(self,*channels):
        for channel in channels:
            cd1 = '0' + str(channel)
            cd2 = 'A' + str(channel)
            self.close(cd1, cd2)
    def openAll(self):
        self.openChannels(1,2,3,4,5,6)


    def closeAll(self):
        self.closeChannels(1,2,3,4,5,6)


