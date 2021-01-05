# @Time : 2020/9/17 17:00 
# @modele : 图片
# @Author : zhengzhong
# @Software: PyCharm

import requests
import time
import os
def count_files(rootDir):
    dirs_all = []
    for root, dirs, files in os.walk(rootDir):

        for d in files:
            m = os.path.join(root, d)
            m1 = m.replace('\\', '/')
            m2 = m1.split("123321")[-1]
            dirs_all.append(m2)
    return dirs_all
local_path = r"C:\Users\Administrator\Desktop\123321"


while True:
    conts = count_files(local_path)
    for remote_file in conts:
        print(remote_file)
        url = "http://192.168.1.249:9999/api/ImageInference"
        data = {
            "sysCode":"1",
            "eqpNo": "test_image",
            "ruleNo": "xxxx",
            "dataType": "local",
            "rawPic": "/home/HwHiAiUser/test_zz"+str(remote_file),
            "recognize": [{
                "para": [{
                        "type": "helmet_detect",
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "pedestrian_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "climbing_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "fence_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "pedestrain_under_crane_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "hang_rail_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "hook_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "fire_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "hole_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "coat_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "sleeve_detect",
                        "conf_thresh": 0.7
                    },
                    {
                        "type": "helmet_wear",
                        "conf_thresh": 0.7
                    }
                ]
            }],
            "reportInfoType":"111",
            "resultUrl":"192.168.1.244:8010"
        }

        a1 = requests.post(url,json=data)
        print(a1.json())
        time.sleep(0.5)

#/hat/kgsgz_0000000318.jpg
#/hat/kgsgz_0000000278.jpg