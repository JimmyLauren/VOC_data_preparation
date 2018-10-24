#coding:utf-8
"""
函数功能：为SSD-caffe检测框架创建test_name_size.trxt
    test_name_size.txt格式如下：
        每一行一个测试样本；
        一行三个数；
        第一个是图像名称，不带后缀
        第二第三个是图像的高度和宽度，H W

    第一步：得到图片的名称;
    第二步：读取图片，得到图片的H和W
    第三步：将图片的名称、图片的H和W分别写入txt文件
	
	注意：路径中的最后一个路径分隔符要是‘\’，因为是以其为标志的
"""

import os
import sys
import cv2

# global settings
# file that save testing image file and xml file
test_img_file='F:\DATASETS\Car_Detection\ShiPinJieGouHua-RenCheJianChe\LMDB/test.txt'
# dir that has testing images
#image_dir='/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train/cashi/JPEGImages'
# test_name_size.txt saving dir
test_name_size_file='F:\DATASETS\Car_Detection\ShiPinJieGouHua-RenCheJianChe\LMDB/test_name_size.txt'

f1=file(test_name_size_file,'a+')

f2=open(test_img_file)
line=f2.readline()
while line:
    print line
    name=line.split('\\')[-1].split('.')[0]  # 图片名称，无后缀
    #temp_image_dir=os.path.join(image_dir,name+'.jpg')

    temp_image_dir=line.split(' ')[0] # 图片的全路径
    im=cv2.imread(temp_image_dir)

    # 图片的形状
    height, width, channels=im.shape

    # 写入文件
    conten=name+' '+str(height)+' '+str(width)+'\n'
    f1.write(conten)

    line=f2.readline()
f1.close()

print "Done!!!!!!!"