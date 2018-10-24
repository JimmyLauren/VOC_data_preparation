#coding:utf-8
from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
 
ImgPath = 'F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/JPEGimages/'
AnnoPath = 'F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/Annotations/'
savepath = 'F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/image_crop/'
 
if not os.path.exists(savepath):
	os.makedirs(savepath)
 
imagelist = os.listdir(ImgPath)
#temp_image_list=imagelist[24888]

i = 0
f=open("fileNotExists.txt","a")
for image in imagelist:
	#标志：一张图片中有多少个object
	count_per_image = 0

	#print 'a new image:', image
	image_pre, ext = os.path.splitext(image)
	imgfile = ImgPath + image 
	xmlfile = AnnoPath + image_pre + '.xml'

	#判断是否存在文件，不存在则continue并将不存在的文件名称保存到txt文件
	if not os.path.exists(imgfile):
		f.write(imgfile)
		f.write('\n')
		continue
	if not os.path.exists(xmlfile):
		f.write(xmlfile)
		f.write('\n')
		continue
	
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
		print objectname
 
 
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

			except Exception, e:
				print e
	i += 1
	print "totally " + str(i) + " images processed"
f.close()
print '\n processed done!!!!!'