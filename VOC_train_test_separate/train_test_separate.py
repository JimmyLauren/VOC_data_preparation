#coding:utf-8
'''
函数功能：将VOC格式数据集按照一定的比例随机划分为测试机和训练集
输出：函数输出一个trainval.txt文件，每一行包含iamge_path和annotation_path
     函数输出一个test.txt，每一行包含image_path和annotation_path

notice: we choose image folder to generate the trainval.txt and test.txt files
        xml file folder can also been used to generate trainval.txt and test.txt file
'''

## global settings here
train_ratio=0.98 # the ratio of training images in whole imageset
image_folder='F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/JPEGimages'
xml_folder='F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/Annotations'
save_folder='F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/LMDB' # folder to save trainval.txt and test.txt files

# libraries importing
import os
import random

# main process
file_names=os.listdir(image_folder) # listing all files within image_folder
num_files=len(file_names) # number of files in folder

train_samples=int(num_files*train_ratio) # the number of train samples

# shuffle file_names file
random.shuffle(file_names)

# generating trainval.txt and test.txt
# generating trainval.txt file
trainval=os.path.join(save_folder,'trainval.txt')
if os.path.exists(trainval):
    os.remove(trainval)
f=file(trainval,'a+')
for i in range(train_samples):
    single_file=file_names[i] # get one file from shuffled file_names
    file_name_pre=single_file.split('.')[0] # getting file name pre

    single_iamge_path=os.path.join(image_folder,file_name_pre)+'.jpg' # single image full path
	# 判断文件是否存在，不存在则继续
    if not os.path.exists(single_iamge_path):
        continue;
	
    single_xml_path=os.path.join(xml_folder,file_name_pre)+'.xml'
	# 判断文件是否存在，不存在则继续
    if not os.path.exists(single_xml_path):
        continue;

    context=single_iamge_path+' '+single_xml_path+'\n'
    f.write(context)
f.close()



# generating test.txt file
test=os.path.join(save_folder,'test.txt')
if os.path.exists(test):
    os.remove(test)
f=file(test,'a+')
for i in range(train_samples,num_files):
    single_file=file_names[i] # get one file from shuffled file_names
    file_name_pre=single_file.split('.')[0] # getting file name pre

    single_iamge_path=os.path.join(image_folder,file_name_pre)+'.jpg' # single image full path
    single_xml_path=os.path.join(xml_folder,file_name_pre)+'.xml'

    context=single_iamge_path+' '+single_xml_path+'\n'
    f.write(context)
f.close()
