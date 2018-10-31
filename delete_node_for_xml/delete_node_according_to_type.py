'''
this function is to delete node for xml files according to their length or height of bncbox
is length or height is smaller than threshold, then delete the corespounding node
'''
import xml.etree.cElementTree as ET
import os

CLASSES = ["10","11"]
threshold=30 # for height and length
path = 'F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/Annotations'
xml_list = os.listdir(path)
for axml in xml_list:
    path_xml = os.path.join(path, axml)
    tree = ET.parse(path_xml)
    root = tree.getroot()

    for child in root.findall('object'):
        name = child.find('name').text
        if name in CLASSES:
            # if their lengths or heights are not qualified
            bndbox=child.find('bndbox')
            xmin=int(bndbox.find('xmin').text)
            xmax=int(bndbox.find('xmax').text)
            ymin=int(bndbox.find('ymin').text)
            ymax=int(bndbox.find('ymax').text)
            height=xmax-xmin
            length=ymax-ymin
            if(height<threshold or length<threshold):
                root.remove(child)
	tree.write(os.path.join('F:/DATASETS/Car_Detection/ShiPinJieGouHua-RenCheJianChe/FinalData/20181019/xmlsnew', axml))
