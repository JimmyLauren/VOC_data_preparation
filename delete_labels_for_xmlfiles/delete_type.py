import xml.etree.cElementTree as ET
import os
#删除xml中不是car的类别
CLASSES = ["car"]
path = '/home/dell/datasets/voc/VOC2007/Annotations'
xml_list = os.listdir(path)
for axml in xml_list:
    path_xml = os.path.join(path, axml)
    tree = ET.parse(path_xml)
    root = tree.getroot()

    for child in root.findall('object'):
        name = child.find('name').text
        if not name in CLASSES:
            root.remove(child)
        tree.write(os.path.join('/home/dell/datasets/voc/VOC2007/aaa', axml))