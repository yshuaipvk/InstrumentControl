from serial import Serial
import time

class TC202:

    def __init__(self,address='COM6'):

        try:
            self.tc202 = Serial(address,9600)
        
        except:
            print('can not find tempurature controler,please check the cable or address')


    # 设置加热功率分为 0%，1%，15%，100%，输入错误时为0%
    def set_power(self,power):
        if power == "1%":
            command = "*01A"+"\r\n"
            #self.tc202.write("*01A")   # 2230 3141 OD00
        elif power ==r"15%":
            command = "2230 3142 0D00" + "\r\n"
            #self.tc202.write("2230 3142 OD00")   # *01B
        elif power ==r"100%":
            command = "2230 3143 0D00" + "\r\n"
            #self.tc202.write("2230 3143 OD00")   # *01C
        else:
            command = "2230 3140 0D00" + "\r\n"
            #self.tc202.write("2230 3140 OD00")   # *01@
        self.tc202.write(command.encode())
        time.sleep(0.01)
        self.tc202.close()


    #设置目标温度
    def set_tempurature(self,value):
        command = "%0100+"+str(value)+"00\r\n"
        self.tc202.write(command.encode())
        time.sleep(0.01)
        #self.tc202.close()


    #读取当前温度
    def read_temperature(self):
        command = "#01"+"\r\n"
        self.tc202.write(command.encode())
        time.sleep(0.01)
        temperature = self.tc202.read_until(size=10)
        temperature = temperature[2:8]
        self.tc202.close()
        return float(temperature)