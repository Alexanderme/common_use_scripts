# @Time : 2020/9/17 17:00
# @modele : 图片
# @Author : zhengzhong
# @Software: PyCharm

import requests
import time
import os
import base64


def count_files(rootDir):
    dirs_all = []
    for root, dirs, files in os.walk(rootDir):

        for d in files:
            m = os.path.join(root, d)
            m1 = m.replace('\\', '/')
            m2 = m1.split("hat")[-1]
            m2 = "/home/HwHiAiUser/datas/no_clothes" + m2
            # print(m2)
            dirs_all.append(m2)
    return dirs_all


local_path = r"C:\Users\Administrator\Desktop\123321\hat\red"


conts = count_files(local_path)

# conts = [file for file in os.listdir(local_path)]

num = 0
while True:
    for remote_file in conts:
        print(remote_file)
        # with open(remote_file, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode()
        url = "http://192.168.1.115:9999/api/ImageInference"
        # print("/home/HwHiAiUser/test_zz/" + str(remote_file)),
        data = {
            "sysCode": "1",
            "eqpNo": "test_image",
            "ruleNo": "xxxx",
            "dataType": "local",
            "rawPic": f"{remote_file}",
            "recognize": [{
                "para": [{
                    "type": "helmet_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "pedestrian_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "climbing_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "fence_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "pedestrain_under_crane_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "hang_rail_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "hook_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "fire_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "hole_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "safety_belts_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "unsafety_belt",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "coat_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "sleeve_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "helmet_wear",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "safety_rope_detect",
                    "conf_thresh": 0.8
                },
                    {
                    "type": "unsafety_rope",
                    "conf_thresh": 0.8
                }
                ]
            }],
            "reportInfoType": "111",
            "resultUrl": "192.168.1.50:8010"
        }

        a1 = requests.post(url, json=data)
        time.sleep(1)
    num += 1
    if num >= 1:
        break
