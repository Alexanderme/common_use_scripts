import requests
import os



count = 0
host = 'http://192.168.1.103:60004'
url_image = '/api/analysisImage'

path = r"J:\测试集与训练集\leaf_test_images"

bad_pics = []
all_wrong_pics = []
info_wrong_pics = []
right_pics = []
def iter_files(rootDir):
    """
    递归遍历所有目录
    :param rootDir:
    :return:
    """
    for root, dirs, files in os.walk(rootDir):
        # 图片访问接口
        if files != []:
            #，有“CB-1”，“YUN-78”， “unknown”三种结果
            variety = root.split("\\")[-1].split("_")
            info_stand = root.split("\\")[-1].split("_")[-1]
            variety_stand = variety[0] +"_" +variety[1]

            if info_stand == "top":
                info_stand = 1
            elif info_stand == "mid":
                info_stand = 2
            elif info_stand == "bottom":
                info_stand = 3
            if variety_stand == "yun_87":
                variety_stand = "YUN-78"
            if variety_stand == "cb_1":
                variety_stand = "CB-1"
            for file in files:
                file_dir = os.path.join(root, file)
                data = {
                    'image': (f'{file}', open(f'{file_dir}', 'rb'))
                }
                try:
                    res_image = requests.post(host + url_image, files=data).json()
                    # print(res_image)
                    alert_flag = int(res_image.get("result").get("alert_flag"))
                    variety = res_image.get("result").get("variety")
                    info = int(res_image.get("result").get("info"))
                    print(f"variety_stand={variety_stand}, info_stand={info_stand}, variety={variety}, info={info}")
                    if alert_flag == 0 or info == 0:
                        all_wrong_pics.append(file)
                        continue
                    if variety != variety_stand:
                        all_wrong_pics.append(file)
                        continue
                    if info != info_stand:
                        info_wrong_pics.append(file)
                    else:
                        right_pics.append(right_pics)
                except Exception as e:
                    bad_pics.append(file)
        for dir in dirs:
            iter_files(dir)


iter_files(path)
a = len(all_wrong_pics)
b = len(info_wrong_pics)
c = len(right_pics)
print(f"all_wrong_pics={a}")
print(f"info_wrong_pics={b}")
print(f"right_pics={c}")
print(len(bad_pics))