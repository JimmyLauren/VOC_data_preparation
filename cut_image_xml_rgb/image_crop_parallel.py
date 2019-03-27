# -*- coding: utf-8 -*-
from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
from random import shuffle
from multiprocessing import Pool
import threading,time
 
ImgPath = u'G:/ErCiFenXi/Datasets/yiji/20190327_赤峰现场难样本标注/JPGImages/'
AnnoPath = u'G:/ErCiFenXi/Datasets/yiji/20190327_赤峰现场难样本标注/xml/'
savepath = u'G:/ErCiFenXi/Datasets/yiji/20190327_赤峰现场难样本标注/crop/'


total_count = 0
def image_crop_parallel(image):
	global total_count
	global ImgPath
	global AnnoPath
	global savepath
	# f=open("fileNotExists.txt","a")
	#标志：一张图片中有多少个object
	count_per_image = 0

	#print 'a new image:', image
	image_pre, ext = os.path.splitext(image)
	imgfile = ImgPath + image 
	xmlfile = AnnoPath + image_pre + '.xml'
	print(imgfile+'\n')
	print(xmlfile+'\n')
	

	#判断是否存在文件，不存在则continue并将不存在的文件名称保存到txt文件
	if not os.path.exists(imgfile):
		#f.write(imgfile)
		#f.write('\n')
		return
	if not os.path.exists(xmlfile):
		#f.write(xmlfile)
		#f.write('\n')
		return
	
	DomTree = xml.dom.minidom.parse(xmlfile)
	annotation = DomTree.documentElement
 
	filenamelist = annotation.getElementsByTagName('filename') #[<DOM Element: filename at 0x381f788>]
	filename = filenamelist[0].childNodes[0].data
	objectlist = annotation.getElementsByTagName('object')

	for objects in objectlist:
		# print objects
		
		namelist = objects.getElementsByTagName('name')
		# print 'namelist:',namelist
		objectname = namelist[0].childNodes[0].data  # 类别###################
		#print objectname
 
 
		bndbox = objects.getElementsByTagName('bndbox')
		cropboxes = []
		for box in bndbox:
			try:
				x1_list = box.getElementsByTagName('xmin')
				x1 = int(x1_list[0].childNodes[0].data)
				y1_list = box.getElementsByTagName('ymin')
				y1 = int(y1_list[0].childNodes[0].data)
				x2_list = box.getElementsByTagName('xmax')
				x2 = int(x2_list[0].childNodes[0].data)
				y2_list = box.getElementsByTagName('ymax')
				y2 = int(y2_list[0].childNodes[0].data)
				w = x2 - x1
				h = y2 - y1

				img = Image.open(imgfile)
				width,height = img.size

				obj = np.array([x1,y1,x2,y2])

				# 对目标物体做微小的移动再裁剪
				# shift = np.array([[0.8,0.8,1.2,1.2],[0.9,0.9,1.1,1.1],[1,1,1,1],[0.8,0.8,1,1],[1,1,1.2,1.2],\
				# 	[0.8,1,1,1.2],[1,0.8,1.2,1],[(x1+w*1/6)/x1,(y1+h*1/6)/y1,(x2+w*1/6)/x2,(y2+h*1/6)/y2],\
				# 	[(x1-w*1/6)/x1,(y1-h*1/6)/y1,(x2-w*1/6)/x2,(y2-h*1/6)/y2]])
                #
				# XYmatrix = np.tile(obj,(9,1))
				# cropboxes = XYmatrix * shift
                #
				# for cropbox in cropboxes:
				# 	# print 'cropbox:',cropbox
				# 	minX = max(0,cropbox[0])
				# 	minY = max(0,cropbox[1])
				# 	maxX = min(cropbox[2],width)
				# 	maxY = min(cropbox[3],height)
                #
				# 	cropbox = (minX,minY,maxX,maxY)
				# 	cropedimg = img.crop(cropbox)
                #
				# 	image_save1=savepath+objectname
				# 	if not os.path.exists(image_save1):
				# 		os.makedirs(image_save1)
				# 	single_save2=image_save1 +'/'+ image_pre + '_' + str(i) + '.jpg'
				# 	cropedimg.save(single_save2,'jpeg')

				cropbox = (x1,y1,x2,y2)
				cropedimg = img.crop(cropbox)

				image_save1=savepath+objectname
				if not os.path.exists(image_save1):
					os.makedirs(image_save1)
				single_save2=image_save1 +'/'+ image_pre + '_' + str(count_per_image) + '.jpg'
				cropedimg.save(single_save2,'jpeg')
				count_per_image=count_per_image+1

			except Exception as e:
				print(e)
	total_count += 1
	print("totally " + str(total_count) + " images processed")
	#f.close()

if __name__=='__main__':
	if not os.path.exists(savepath):
		os.makedirs(savepath)
	# 先锁死，完成后再开锁
	lock=threading.Lock()
	imagelist = os.listdir(ImgPath)
	# temp_image_list=imagelist[24888]
	shuffle(imagelist)
	pool=Pool(5)
	rl=pool.map(image_crop_parallel,imagelist)
	pool.close()
	pool.join()
	rl

	#start_time=time.time()
	# for image in imagelist:
	# 	# lock.acquire()
	# 	# try:
	# 	# 	th=threading.Thread(target=image_crop_parallel,args=(image,))
	# 	# 	th.start()
	# 	# 	#image_crop_parallel(image)
	# 	# finally:
	# 	# 	lock.release()
	print('\n processed done!!!!!')
