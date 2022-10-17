# SEM图片查找晶界
#通过对图片进行灰度化、二值化

import cv2
import numpy as np
import os

address_ = 'F:\GYR\\MA-5MACl_i025.tif'


def pictureProcess(address):
    img = cv2.imread(address)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = gray[:3500, :]
    # gray=gray[:1000,:800]
    # gray=svd_(gray,200)
    gray = cv2.blur(gray, (8, 8))
    gray = gray.astype(np.uint8)
    ret, binary = cv2.threshold(gray, 138, 255, cv2.THRESH_BINARY)
    # contours,hierarchy=cv2.findContours(binary,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_TC89_L1)
    # a=cv2.drawContours(binary,contours,-1,(255,0,0),1)
    area = 0
    for i in range(binary.shape[0]):
        for j in range(binary.shape[1]):
            if binary[i][j] == 0:
                area += 1
    total = gray.shape[0] * gray.shape[1]
    percent = area / total
    print('GB area:{}'.format(area))
    print('total area:{}'.format(total))
    print('percent:{}'.format(percent))

    # cv2.imwrite('black_.png',binary)
    cv2.imshow('dead', binary)
    # cv2.imwrite('1_new.png',binary)
    # return total,area,percent,binary
    cv2.waitKey(0)
    cv2.destroyAllWindows()


pictureProcess(address_)
# root_address='F:\GYR'
# filenames=os.listdir(root_address)
# result=[]
# for filename in filenames:
#    print(filename)
#    file_dir=os.path.join(root_address,filename)
#    total,area,percent,picture=pictureProcess(file_dir)
#    new_filename='new_'+filename
#    new_file_dir=os.path.join(root_address,new_filename)
#    cv2.imwrite(new_file_dir,picture)
