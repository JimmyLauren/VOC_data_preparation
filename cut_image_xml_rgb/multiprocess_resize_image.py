# -*- coding: utf-8 -*-
#multiprocessing template
import multiprocessing
import cv2
import os
import time
from PIL import Image
import datetime
from numpy import*
"""
******输入参数*******
"""
imgroot = '/media/huang/f562dcdc-677a-4a77-8c08-cb4432080c371/maincar_chifeng/'
outputpath = '/media/huang/f562dcdc-677a-4a77-8c08-cb4432080c371/maincar_chifeng_resize180/'  #自带创建文件夹
imgtype = 'jpg'
processNumber = 180
resize_size = (180,180)
printNum = 0
"""
*********************
"""
#读取文件路径
def read_data_path2(data_path,hidename):
    """
    内部功能函数：对文件夹路径下文件的进行搜索，并对其文件格式进行筛选
    :param data_path: 文件夹路径
    :param hidename: 文件筛选格式
    :return: 返回2个列表[filename][filepath]
    """
    #遍历文件夹内所有文件
    outputpath = []
    count=0
    for dirpath, dirnames, filenames in os.walk(data_path):
        for filename in filenames:
            # if dirpath.split('/media/huang/f562dcdc-677a-4a77-8c08-cb4432080c371/maincar/')[1] !=78:
            #    continue
            filePath=dirpath+'/'+filename
            # image = cv2.imdecode(np.fromfile(filePath), dtype=np.uint8), -1)
            # im = cv2.imread(filePath)
            # if im is None:
            #     print  filePath
            #     continue
            #进行扩展名筛选
            # try:
            #     img = Image.open(filePath)
            # except IOError:
            #     print  filePath
            #     continue
            # try:
            #     img = np.array(img, dtype=np.float32)
            # except:
            #     print  filePath
            #     continue
            if os.path.splitext(filename)[1] == ('.' + hidename) :
                # label=dirpath.split('/home/huang/2maincar/data/')[1]
                path = [dirpath ,filename]
                count = count+1
                outputpath.append(path)
    return outputpath

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"

    else:
        print "---  There is this folder!  ---"


def write_file(result):
    if outputpath[-1] != '/':
        print "your path lack /"
    else :
        output_path = outputpath +result[2]+'/'+result[0]  #+ result[2]+'/'
        cv2.imwrite(output_path ,result[1])
        global printNum
        printNum = printNum + 1
        # print  '%s %d'%(result[0],printNum)

def process(imgpath,label):
    src = cv2.imread(os.path.join(imgpath[0] , imgpath[1]))

    dst = cv2.resize(src ,resize_size)
    #print imgpath[1]
    result = [imgpath[1],dst,label]
    # print imgpath[1] + ' ' + label + '\n'
    return result

def main():
    # 设置进程数
    pool = multiprocessing.Pool(processes=processNumber)
    #判断并创建文件
    for i  in  range(150):
        print '任务' + str(i)
        # if i !=78:
        #     continue
        # if i==76:
        #     break
        savePath=outputpath+str(i)
        mkdir(savePath)
        start = datetime.datetime.now()

    #处理每个文件加中图片
        outputTxt = outputpath +str(i)+'.txt'
        imgroot2=imgroot+str(i)
        imgpath = read_data_path2(imgroot2, imgtype)
        file = open(outputTxt ,'w')

        # count =0
        for img in imgpath:
        #将任务导入进程
            pool.apply_async(process, (img,str(i)),callback=write_file)  # process will return result,id is input ,write_file will accept the result from process.
        #写出txt文件
            file.write(img[1] + ' ' + str(i) + '\n')
        # file.write(img[1] ++' '+ img[2] + '\n')
        #    count=count+1
        #    if count>30:
        #         break


        end = datetime.datetime.now()
        print end-start
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
