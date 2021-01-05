"""
    #  @ModuleName: clearn_xml.py
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/20 11:53
"""
import os
import time

import requests
from bs4 import BeautifulSoup


def clear_dir():
    if os.path.exists("xml.txt"):
        os.remove("xml.txt")


def xmls_create(xml_path):
    # 一比all  点标注形式
    # name_txt = i.split('.')[0] + ".txt"
    with open(xml_path, "rb") as f:
        a1 = f.read()
    soup = BeautifulSoup(a1, 'lxml')
    object_all = soup.find_all("image")
    for object in object_all:
        images_name = object['name'].split("/")[-1]
        images_points = object.find_all("points")
        person_count = str(len(images_points))
        txt_create(images_name, person_count)

    print("xml文件txt生成完毕========================================")



def txt_create(image_file, person_count):

    img_path = os.path.join(path, image_file)
    with open(img_path, "rb") as f:
        fb = f.read()
    data = {
        "image": fb,
    }
    a2 = requests.post(url, files=data)

    res_num = a2.json().get("result").get("people_num")
    print(res_num)
    if int(res_num) != int(person_count):
        global error_count
        error_count += 1
    else:
        global right_count
        right_count += 1



right_count = 0
error_count = 0
path = r"G:\数据\人流密度\KSTperson20201014done\KSTperson20201014done\img"
url = "http://192.168.1.103:60001/api/analysisImage"
xmls_create("G:\数据\人流密度\KSTperson20201014done\KSTperson20201014done\KSTperson20201014.xml")
print(error_count, right_count, right_count/(right_count+error_count))

