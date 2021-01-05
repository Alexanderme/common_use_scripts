from bs4 import BeautifulSoup
import os
import requests
import time
from clear_dirs import clear

BASE_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
RES_DIR = os.path.abspath(os.path.join(os.path.abspath(BASE_DIR), "input"))

# 要移动的路径
res_xml_path = os.path.join(RES_DIR, "ground-truth")
# 要移动的结果路径
res_txt_path = os.path.join(RES_DIR, 'detection-results')


def xml_create(xml_path):
    # 一比一
    a1 = [file for file in os.listdir(xml_path) if file.lower().endswith('xml')]
    num = 0
    for j in a1:
        num += 1
        print(f"开始生成xml文件txt{num}")
        name_txt = j.split('.')[0] + ".txt"
        with open(os.path.join(xml_path, j), "rb") as f:
            a1 = f.read()
        soup = BeautifulSoup(a1, 'lxml')
        object_all = soup.find_all("object")
        for i in object_all:
            name = i.find_all("name")[0].string
            if name.endswith("helmet"):
                name = "hat"
            for m in i.find_all("bndbox"):
                xmin = m.find_all("xmin")[0].string
                ymin = m.find_all("ymin")[0].string
                xmax = m.find_all("xmax")[0].string
                ymax = m.find_all("ymax")[0].string
                with open(os.path.join(res_xml_path, name_txt), "a") as f:
                    f.write("%s %s %s %s %s\n" % (
                        name, int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax))))
    print("xml文件txt生成完毕========================================")



def txt_create(img_path):
    s = time.time()
    a1 = [file for file in os.listdir(img_path) if file.endswith('jpg')]
    num = 0
    for i in a1:
        num += 1
        url = "http://192.168.1.103:50001/api/analysisImage"
        with open(os.path.join(img_path, i), "rb") as f:
            fb = f.read()
        data = {
            "image": fb,
        }
        a2 = requests.post(url, files=data)
        res_index = a2.json().get("result").get("headInfo")
        print(a2.json().get("result"))
        # res_base64 = a2.json().get("buffer")
        # image_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
        # res_image = base64.decodebytes(res_base64.encode('ascii'))
        # with open(f'res/{image_name}.jpg', 'wb') as f:
        #     f.write(res_image)
        if res_index is None or res_index == [] or res_index == 'null':
            name_txt = i.split('.')[0] + ".txt"
            with open(os.path.join(res_txt_path, name_txt), "a") as f:
                f.write("\n")
            continue
        for r in res_index:
            try:
                print(r)
                # GPU 安全帽
                name_txt = i.split('.')[0] + ".txt"
                numOfHelmet = r.get("numOfHelmet")
                if int(numOfHelmet) == 1:
                    name = "hat"
                if int(numOfHelmet) == 0:
                    name = "head"
                # name = r.get("name")
                # if name == "helmet":
                #     name = "hat"
                # name = r.get("name")
                # name = "character"
                confidence = "1"
                x = r["x"]
                y = r["y"]
                width = r["width"]+x
                height = r["height"]+y
                # x = r["xmax"]
                # y = r["ymax"]
                # xmin = r["xmin"]
                # ymin = r["ymin"]
                # import cv2
                # print(os.path.join(img_path, i))
                # image = cv2.imread(os.path.join(img_path, i))
                #
                # cv2.rectangle(image, (x, y), (width, height), (0, 255, 255), 2)
                # # cv2.imwrite(r'C:\Users\Administrator\Desktop\2', i)
                # cv2.imwrite(r'C:\Users\Administrator\Desktop\2\%s' % i, image)

                with open(os.path.join(res_txt_path, name_txt), "a") as f:
                    f.write("%s %s %s %s %s %s\n" % (name, confidence, x, y, width, height))
            except Exception as e:
                name_txt = i.split('.')[0] + ".txt"
                with open(os.path.join(res_txt_path, name_txt), "a") as f:
                    f.write(" \n")
    e = time.time()
    u = e - s
    print(u)


clear()
path = r"J:\数据\安全帽\20201125\HRhat_clothes20201118test\HRhat_clothes20201118test"
# xml_create(path)
txt_create(path)
