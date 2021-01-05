import requests
import os

count = 0
host = 'http://192.168.1.136:60026'
url_image = '/api/analysisImage'

path = r"C:\Users\Administrator\Desktop\1"

bad_pics = []
all_wrong_pics = []
info_wrong_pics = []
right_pics = []
num = 0


def iter_files(rootDir):
    """
    递归遍历所有目录
    :param rootDir:
    :return:
    """

    for root, dirs, files in os.walk(rootDir):
        # 图片访问接口
        if files != []:
            # ，有“CB-1”，“YUN-78”， “unknown”三种结果
            variety_stand = root.split("\\")[-3]
            # 1 上部叶， 2 中部叶， 3 下部叶
            info_stand = root.split("\\")[-1][:2]
            if info_stand == "上部":
                info_stand = 1
            elif info_stand == "中部":
                info_stand = 2
            elif info_stand == "下部":
                info_stand = 3
            if variety_stand == "云-87":
                variety_stand = "YUN-78"
            for file in files:
                global num
                num += 1
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
                    print(f"当前识别的图片名称是{file}")
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
                        right_pics.append(file)
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
