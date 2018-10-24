# -*- coding: utf-8 -*-
"""

"""
import os
import os.path
import numpy as np
import xml.etree.ElementTree as xmlET
from PIL import Image, ImageDraw

classes = ('__background__', # always index 0
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

file_path_img = '/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train/im'
file_path_xml = '/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train/xml'
save_file_path = '/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train'

pathDir = os.listdir(file_path_xml)
for idx in xrange(len(pathDir)):  
    filename = pathDir[idx]
    tree = xmlET.parse(os.path.join(file_path_xml, filename))
    objs = tree.findall('object')        
    num_objs = len(objs)
    boxes = np.zeros((num_objs, 5), dtype=np.uint16)

    for ix, obj in enumerate(objs):
        bbox = obj.find('bndbox')
        # Make pixel indexes 0-based
        x1 = float(bbox.find('xmin').text) - 1
        y1 = float(bbox.find('ymin').text) - 1
        x2 = float(bbox.find('xmax').text) - 1
        y2 = float(bbox.find('ymax').text) - 1

        cla = obj.find('name').text 
        label = cla

        boxes[ix, 0:4] = [x1, y1, x2, y2]
        boxes[ix, 4] = label

    image_name = os.path.splitext(filename)[0]
    img = Image.open(os.path.join(file_path_img, image_name + '.jpg')) 

    draw = ImageDraw.Draw(img)
    for ix in xrange(len(boxes)):
        xmin = int(boxes[ix, 0])
        ymin = int(boxes[ix, 1])
        xmax = int(boxes[ix, 2])
        ymax = int(boxes[ix, 3])
        draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))

        kk=boxes[ix, 4]
        #draw.text([xmin, ymin], classes[boxes[ix, 4]], (255, 0, 0))
        draw.text([xmin, ymin], str(boxes[ix, 4]), (255, 0, 0))

    img.save(os.path.join(save_file_path, image_name + '.png'))
