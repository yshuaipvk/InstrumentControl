# 示波器
import pyvisa as visa
import struct


class HDO4054A():
    def __init__(self, address='TCPIP0::169.254.75.166::inst0::INSTR'):
        try:
        # address = 'TCPIP0::169.254.164.203::inst0::INSTR'
            rm = visa.ResourceManager()
            self.scope = rm.open_resource(address)
            self.scope.write('CORD HI;CHDR OFF')
        except:
            print("Can not find scope,please check the cable or address")
    def time_base(self, tdiv, tdl, point):
        # check done
        # set time base: second/div,time delay=-4*second/div
        self.scope.write('TDIV ' + str(tdiv) + ';TRDL ' + str(tdl) + ';MSIZ ' + str(point) + ';')

    def configure_channel(self, channel, volt, offset):
        # configure channel  V/div   offset(V)
        # self.scope.write('''C2:VDIV 0.2;C2:OFST -0.6;''')
        self.scope.write(str(channel) + ':VDIV ' + str(volt) + ';' + channel + ':OFST ' + str(offset) + ';')

    def configure_sweep(self, sweep):
        # check done
        self.scope.write(''' VBS 'app.acquisition.C2.AverageSweeps=''' + str(sweep))

    def configure_saving(self, channel, filename, fileAddress):
        # check done
        # configure channel,filename,address; default:ASCII,Comma
        # the command form is:      '''VBS 'app.SaveRecall.Waveform.SaveSource = "C1" '''
        self.scope.write('''VBS 'app.SaveRecall.Waveform.SaveSource = "''' + channel + '''":'''
                          '''app.SaveRecall.Waveform.SaveTo = "File" :
                           app.SaveRecall.Waveform.TraceTitle = "''' + filename + '''":'''
                           '''app.SaveRecall.Waveform.WaveFormat = "ASCII" :
                            app.SaveRecall.Waveform.Delimiter="Comma":
                             app.SaveRecall.Waveform.WaveformDir = "''' + fileAddress + '''" ';*OPC?''')

    def save_data_in_scope(self):
        # check done
        # save data in scopp not in PC
        self.scope.write(
            '''VBS? 'app.SaveRecall.Waveform.DoSave : return=app.SaveRecall.Waveform.SaveFilenamePreview''')

    def visa_close(self):
        self.scope.close()

    def stop(self):
        self.scope.write('TRMD STOP')

    def start(self):
        self.scope.write('TRMD NORM')

    def configure_trigger_source(self, channel):
        self.scope.write('TRSE EDGE,SR,%s' % channel)

    def configure_trigger_slope(self, channel, slope):
        if slope == 1:
            self.scope.write('%s:TRSL POS' % channel)
        if slope == 2:
            self.scope.write('%s:TRSL NEG' % channel)

    def configure_sample_mode(self, mode='RealTime'):
        # mode: RealTime,RIS,Sequence,Roll,WaveStream
        self.scope.write('''VBS 'app.Acquisition.Horizontal.SampleMode="''' + mode + '''"''')

    #def gain_sweep_statistics(self):
    #  self.scope.write('PAST? PARAM')
    # return self.scope.read_raw(10)   error
    def activate_channel(self, channel):  # 打开chennel
        self.scope.write(channel + ':TRA ON;')

    def deactivate_channel(self, channel):  # 关闭channel
        self.scope.write(channel + ':TRA OFF')

    def clear_sweep(self):  # 清空sweep，即从0开始累积
        self.scope.write('CLSW')


    def get_sweeps(self,channel):
        # unchecked
        self.scope.write("app.Acquisition.{}.Out.Result.Sweeps".format(channel))
        sweeps = self.scope.read_raw(128)
        return sweeps


    def get_waveform(self, channel):
        # 默认commnad_type为WORD即 command_type==1
        # self.scope.write('*CLS;ARM;FRTR')
        self.scope.write('WFSU SP,0,NP,0,FP,0,SN,0')
        self.scope.write('CFMT DEF9,WORD,BIN')  # 此处设置为WORD  此外也可以设置为BYTE
        self.scope.write('%s:WF? DESC' % channel)
        describe = self.scope.read_raw(10000)
        # 返回16进制数据 分别解码得到相应参数
        describe = describe[16:]
        command_type = struct.unpack('>h', describe[32:34])
        first_vaild_point = struct.unpack('>i', describe[124:128])
        last_vaild_point = struct.unpack('>i', describe[128:132])
        vertical_offset = struct.unpack('>f', describe[160:164])
        vertical_gain = struct.unpack('>f', describe[156:160])
        horizontal_interval = struct.unpack('>f', describe[176:180])
        number_of_point = struct.unpack('>i', describe[116:120])
        horizontal_offset = struct.unpack('>d', describe[180:188])
        # 将describe生成列表方便后续调用
        describe_list = command_type + first_vaild_point + last_vaild_point + vertical_offset + vertical_gain + horizontal_interval + \
                        number_of_point + horizontal_offset

        self.scope.write('%s:WF? DAT1' % channel)
        data = []
        # 获取Y值
        if describe_list[0] == 0:  # 等于0是为byte 一个字节表示一个数据
            byte_count = describe_list[6] + 17
            data_byte = self.scope.read_raw(byte_count)
            for i in range(describe_list[6]):
                arr = struct.unpack('>b', data_byte[i:i + 1])[0]  # arr返回的是含一个元素元组，引索第一个元素
                arr = arr * describe_list[4] - describe_list[3]
                arr = arr * describe_list[4] - describe_list[3]
                x, y = i * describe_list[5] + describe_list[-1], arr
                data.append((x, y))
        else:  # command_type=1时为word 2个字节表示一个数据  默认为WORD
            byte_count = 2 * describe_list[6] + 17
            data_byte = self.scope.read_raw(byte_count)
            data_byte = data_byte[16:]
            # 分别解码得到数据
            for i in range(describe_list[6]):
                arr = struct.unpack('>h', data_byte[2 * i:2 * i + 2])[0]  # arr返回的是含一个元素元组，引索第一个元素
                arr = arr * describe_list[4] - describe_list[3]
                # x_value.append(i * describe_list[5] + describe_list[-1])
                # y_value.append(arr)
                x, y = i * describe_list[5] + describe_list[-1], arr
                data.append((x, y))
        return data  # data数据格式为  x1,y1
        #                             x2,y2
        #                             x3,y3

    def set_couple(self, channel, couple):  # 设置采样电阻，D1M, D50, A1M, GND
        self.scope.write(channel + ':CPL ' + couple)

    def trigger_couple(self, channel, couple):  # DC,AC
        self.scope.write(channel + ':TRCP ' + couple)


import os
import numpy as np



if __name__ == '__main__':
    
    scope = HDO4054A()
    data = scope.get_waveform('C2')
    rootdir = r"D:\ys\DATA\fs激光器同步信号"
    if not os.path.exists(rootdir):
        os.mkdir(rootdir)
    file_des = "psAndFsChopper.txt"
    save_root = os.path.join(rootdir,file_des)
    np.savetxt(save_root,data,delimiter=',')