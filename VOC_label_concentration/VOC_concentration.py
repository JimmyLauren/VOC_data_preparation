# coding:utf-8
"""
function:实现将车牌检测的标签合并（对于骑车人和两轮车而言，需要更改合并后的bounding box）
	input:1、需要修改的标签文件路径（不加“/”）;
		2、新的标注文件保存路径地址；
		3、需要修改的标签类型；
	output:新的标注文件。
"""

import numpy as np
import os
import xml.etree
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


# 全局设置在这里
"""
更换标签后标签含义：
1：车窗    2：车脸    3：车身    4：二轮车    5:三轮车    6：骑车人    7：行人    8：后脸
"""
# 建立新旧标签映射表
old2new = {'1':3, '3':2, '4':3, '5':1, '6':2, '7':3, '10':3, '13':3,
'16':3, '18':2, '19':4, '20':5, '33':6, '34':7, '35':8, '36':8}

file_old = "/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train/cashi/Annotations"
file_new = "/media/liujian1/Ubuntu/DATASETS/Car_Detection/VOC_cardetection/train/cashi/Annotations_new"
find_tags = './object/name'


def read_xml(in_path):
    """
    读取并解析xml文件
    :param in_path: xml路径
    :return: ElementTree
    """
    tree=ElementTree.parse(in_path)
    return tree

#------------ change the tree file iteratively ---------
def find_change_nodes(root_node):
    """ 一次处理一个文件
    递归修改root_node里的属性,先改后删除
    :param root_node: 初始输入root
    :return: 修改过后新的root
    """
    # 对节点进行处理
    tag=root_node.tag
    if tag=='object':
        # 对包含'object'标签的节点进行操作，修改对应的标签值
        name_temp=root_node.getchildren()[0].text
        if ('2'!=name_temp):
            # 标签不是混杂的(2)和两轮车(19)以及骑车人(33)
            debug=old2new[name_temp]
            root_node.getchildren()[0].text=str(debug)
        return
    # 若不是包含'object'标签的node，继续进行递归操作
    else:
        children_node=root_node.getchildren()
        for child in children_node:
            find_change_nodes(child)
        return

def write_xml(tree,out_path):
    """
    将文件写出
    :param tree: xml树
    :param out_path: 写出路径
    :return: 无
    """
    tree.write(out_path,encoding='utf-8',xml_declaration=None)




if __name__=="__main__":
    # # test
    # xml=file_old+'/'+'301.xml'
    # tree=read_xml(xml)
    # root=tree.getroot()
    # find_change_nodes(root)


    files = os.listdir(file_old)
    counter=0

    # 得到所有的标签文件、按标签名字找到对应的值、更改标签对应的值
    # files为标签文件xml文件
    for file in files:
        counter=counter+1
        print str(counter)+' files have been processed!\n'

        xml_file = file_old + '/' + file  # 完整的xml文件路径
        tree=read_xml(xml_file)  # 解析xml文件
        new_tree=tree
        root=tree.getroot()

        # 修改合并tree中的标签
        find_change_nodes(root)

        # 删除tree中的“2”标签所在的“object”
        for child in root.getchildren():
            if 'object'==child.tag:
                if '2'==child.getchildren()[0].text:
                    # 删除‘2’标签的‘object’
                    #print '-----------'
                    root.remove(child)

        new_tree._root=root


        write_xml(new_tree,file_new+'/'+file)
