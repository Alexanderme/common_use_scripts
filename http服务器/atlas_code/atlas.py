import requests
import json
import os
import time
import base64


path = r"G:\数据\atls\样本图片\pati"

images = [file for file in os.listdir(path)]

path = "/home/HwHiAiUser/ljx_test/pati"

while True:
    for image in images:
        image = os.path.join(path, image)
        image = image.replace("\\", "/")

        # with open(image, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode()
        url = "http://192.168.1.115:9999/api/ImageInference"
        data = {
            "sysCode": "1",
            "eqpNo": "test_image",
            "ruleNo": "xxxx",
            "dataType": "local",
            "rawPic": f"{image}",
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
            "reportInfoType": "101",
            "resultUrl": "192.168.1.50:8010"
        }
        time.sleep(1)
        res = requests.post(url, data=json.dumps(data))
        print(res.json())
