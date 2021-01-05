import os
import requests
import time
from xml.etree.ElementTree import parse
import chardet

import re

# 1:  xml是否包含中文  2:命名是否规范  3:图片是否能打开  4:图片和xml名字是否匹配  5:算法运行图片是否正常得到结果  6:查看xml文件类型



path = r"G:\数据\q3\Q3_RIGHT\Q3\motorhelmet_right"
url = "http://192.168.1.147:60002/api/analysisImage"
# 总xml数目
xml_files = []
# 总图片数目
pic_files = []
# 总错误图片数目
wrong_files = []
# xml和图片总数
file_count = 0
# 名称不对应的xml和图片
xml_pic_not_match = {}
# 错误图片 打不开图片
wrong_pic = []
# 错误的xml
wrong_xml_with_other_tag = []
wrong_xml_with_float = []
wrong_xml_unicode = []
# xml种类
xml_kinds = ["motor", "head", "helmet"]
contains_chinese_pic = []


def iter_files(rootDir):
    """
    递归遍历所有目录
    :param rootDir:
    :return:
    """
    for root, dirs, files in os.walk(rootDir):
        global file_count
        file_count += len(files)
        # 调用函数判断基础图片数据是否正常 并且分类好图片和xml
        if not check_pic_num(root, files) or len(wrong_files) > 0:
            print("图片数目和xml数目对应不上, 基础数据不是以jpg,xml结尾")
            print(wrong_files)
        # xml和图片命名是否一致
        check_datas_name()
        for dir in dirs:
            iter_files(dir)


def check_pic_num(root, files):
    """
    用于统计xml_file, pic_file,wrong_file 中图片是否是以jpg, xml命名,不是的话就会报错
    :return:
    """
    for file in files:
        if file.endswith("xml"):
            xml_files.append(os.path.join(root, file))
        elif file.endswith("jpg"):
            pic_files.append(os.path.join(root, file))
        else:
            wrong_files.append(os.path.join(root, file))
    return len(xml_files) + len(pic_files) + len(wrong_files) == file_count


def check_datas_name():
    """
    xml和图片命名是否一致
    :param data:
    :return:
    """
    for xml, pic in zip(xml_files, pic_files):
        if xml.split(".")[0] != pic.split(".")[0]:
            xml_pic_not_match[pic] = xml


def get_http_ias(pic_files):
    """
    调用ias接口判断图片是否打不开
    :return:
    """
    for pic_with_dir in pic_files:
        pic = pic_with_dir.split("\\")[-1]
        data = {
            'image': (pic, open(pic_with_dir, 'rb'))
        }
        try:
            res_image = requests.post(url, files=data)
            if res_image.json().get("code") == -1:
                print("------------------算法未授权, 退出-----------------")
                print(pic_with_dir)
        except Exception as e:
            print("报错的图片{}".format(pic_with_dir))
            wrong_pic.append(pic)
            time.sleep(10)
            return None

def get_xml_res():
    """
    获取xml中的类型和坐标  检查是否存在多余标签 检查是否存在数字坐标
    :paramer  传入xml绝对路径 以列表返回每个xml文件内容
    """
    for xml in xml_files:
        doc = parse(xml)
        root = doc.getroot()
        res_kinds = doc.iterfind('object/name')
        res_coordinates = doc.iterfind('object/bndbox')
        for res_kind in res_kinds:
            if res_kind.text not in xml_kinds:
                wrong_xml_with_other_tag.append(xml)
                tfs = root.findall("./object[name='plate']")
                for tf in tfs:
                    root.remove(tf)
                    doc.write(xml, xml_declaration=True)
        for res_coordinate in res_coordinates:
            ymin = res_coordinate.find('ymin').text
            xmin = res_coordinate.find('xmin').text
            ymax = res_coordinate.find('ymax').text
            xmax = res_coordinate.find('xmax').text
            if '.' in ymin or '.' in xmin or '.' in ymax or '.' in xmax:
                if xml not in wrong_xml_with_float:
                    wrong_xml_with_float.append(xml)

                    res_coordinates_ymin = root.findall('object/bndbox/ymin')
                    res_coordinates_ymax = root.findall('object/bndbox/ymax')
                    res_coordinates_xmin = root.findall('object/bndbox/xmin')
                    res_coordinates_xmax = root.findall('object/bndbox/xmax')

                    for res_coordinate in res_coordinates_ymin:
                        ymin = int(float(res_coordinate.text))
                        res_coordinate.text = str(ymin)
                        doc.write(xml, xml_declaration=True)
                    for res_coordinate in res_coordinates_ymax:
                        ymax = int(float(res_coordinate.text))
                        res_coordinate.text = str(ymax)
                        doc.write(xml, xml_declaration=True)

                    for res_coordinate in res_coordinates_xmin:
                        xmin = int(float(res_coordinate.text))
                        res_coordinate.text = str(xmin)
                        doc.write(xml, xml_declaration=True)

                    for res_coordinate in res_coordinates_xmax:
                        xmax = int(float(res_coordinate.text))
                        res_coordinate.text = str(xmax)
                        doc.write(xml, xml_declaration=True)




def check_file_unicode():
    """
    判断xml类型是不是utf-8
    :param xml_file:
    :return:
    """
    for xml_file in xml_files:
        with open(xml_file, 'rb') as f:
            data = f.read()
            if chardet.detect(data).get("encoding") != 'ascii':
                wrong_xml_unicode.append(xml_file)



def jude_chinese(pic_files):
    for pic in pic_files:
        pic = pic.split("\\")[-1]
        pattern = re.compile(u"[\u4e00-\u9fa5]+")
        result = re.findall(pattern, pic)
        if result:
            contains_chinese_pic.append(pic)





iter_files(path)
# get_http_ias(pic_files)
get_xml_res()
# check_file_unicode()
# jude_chinese(pic_files)
print(f"contains_chinese_pic={contains_chinese_pic}")
print("xml_pic_not_match{}".format(xml_pic_not_match))
print("wrong_pic{}".format(wrong_pic))
print("wrong_xml_with_other_tag{}".format(wrong_xml_with_other_tag))
with open('1.txt', 'wt', encoding='utf-8') as f:
    f.write(str(wrong_xml_with_float))
print("wrong_xml_with_float{}".format(wrong_xml_with_float))
print("wrong_files{}".format(wrong_files))
print(f"wrong_xml_unicode{wrong_xml_unicode}")

# 格式化xml
import xml.etree.ElementTree as ET


def prettyXml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
    # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作
    return element


from xml.etree import ElementTree  # 导入ElementTree模块

for xml in xml_files:
    tree = ElementTree.parse(xml)  # 解析test.xml这个文件，该文件内容如上文
    root = tree.getroot()  # 得到根元素，Element类
    root = prettyXml(root, '\t', '\n')  # 执行美化方法
    # ElementTree.dump(root)  # 打印美化后的结果
    tree = ET.ElementTree(root)  # 转换为可保存的结构
    tree.write(xml)  # 保存美化后的结果
