# @Time : 2020/9/18 10:35
# @modele : 视频流
# @Author : zhengzhong
# @Software: PyCharm
config_url = {
    "uuid1": "rtsp://admin:extremevision201@192.168.1.138/ch1/main/av_stream",
    "uuid2": "rtsp://admin:extremevision201@192.168.1.35/ch1/main/av_stream",
    "uuid3": "rtsp://admin:Hyc19950423@192.168.1.66:554/h264/ch1/main/av_stream"
}
config_bendi = {
    "uuid1": "/home/HwHiAiUser/datas/video/1.mp4",
    "uuid2": "/home/HwHiAiUser/datas/video/2.avi"
}
config_url_test = {
    "uuid1": "192.168.1.51:8010",
    "uuid2": "192.168.1.244:8010"
}

import requests
import time
import random
# 视频流启动


def video_url(name, video, result_url):
    url = "http://192.168.1.115:9999/api/StartVideoInference"
    t = []
    data = {
        "sysCode": name[0],
        "ruleNo": name[1],
        "dataType": "remote",
        "sendStream": "1",
        "videoUrl": {
            "remote_rtsp": [{
                    "eqpNo": name[2],
                    "rtsp": video
            }
            ]
        },
        "reportType": 1,
        "normalReportFre": 20,
        "abnormalReportFre": 10,
        "recognize": [{
            "eqpNo": name[2],
            "para": [
                {
                    "type": "helmet_detect",
                    "sampleFre": 0.5,
                    "conf_thresh": 0.2
                },
                {
                    "type": "pedestrian_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "climbing_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "fence_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "pedestrain_under_crane_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "hang_rail_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "hook_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "fire_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "hole_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "coat_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "sleeve_detect",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                },
                {
                    "type": "helmet_wear",
                    "sampleFre": 0.1,
                    "conf_thresh": 0.2
                }
            ]
        }
        ],
        "reportInfoType": "010",
        "resultUrl": result_url
    }
    a1 = requests.post(url, json=data)
    print(a1.json())
    t.append(data.get("sysCode"))
    t.append(data.get("ruleNo"))
    t.append(data.get("recognize")[0].get("eqpNo"))
    return tuple(t)


# 本地视频启动
def bendi_video(name, video, result_url):
    url = "http://192.168.1.115:9999/api/StartVideoInference"
    t = []
    data = {
        "sysCode": name[0],
        "ruleNo": name[1],
        "dataType": "local",
        "sendStream": "1",
        "videoUrl": {
            "local_video": [
                {
                    "eqpNo": name[2],
                    "video": video
                }
            ]
        },
        "reportType": 1,
        "normalReportFre": 2,
        "abnormalReportFre": 2,
        "recognize": [
            {
                "eqpNo": name[2],
                "para": [
                    {
                        "type": "pedestrain_under_crane_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "pedestrian_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "climbing_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "fence_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "pedestrain_under_crane_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "hang_rail_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "hook_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "fire_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "hole_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "coat_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "sleeve_detect",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    },
                    {
                        "type": "helmet_wear",
                        "sampleFre": 0.1,
                        "conf_thresh": 0.2
                    }
                ]
            }
        ],
        "reportInfoType": "111",
        "resultUrl": result_url
    }
    a1 = requests.post(url, json=data)
    print(a1.json())
    t.append(data.get("sysCode"))
    t.append(data.get("ruleNo"))
    t.append(data.get("recognize")[0].get("eqpNo"))
    return tuple(t)


def stop_video(name):
    url = "http://192.168.1.115:9999/api/StopVideoInference"
    data = {
        "sysCode": name[0],
        "ruleNo": name[1],
        "eqpNo": name[2],
        "videoUrl": "rtsp://admin:admin@192.168.1.145:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
    }
    a1 = requests.post(url, json=data)
    print(a1.json())


def uuid_test():
    import uuid
    uid1 = str(uuid.uuid4())
    uid2 = str(uuid.uuid4())
    uid3 = str(uuid.uuid4())
    suid1 = ''.join(uid1.split('-'))
    suid2 = ''.join(uid2.split('-'))
    suid3 = ''.join(uid3.split('-'))
    return (suid1, suid2, suid3)


if __name__ == '__main__':

    t_list = []
    while len(t_list) < 5:
        uid = uuid_test()
        if random.randint(1, 999) % 2 == 0:
            name = video_url(uid, video=config_url[f"uuid{random.randint(1,3)}"],
                             result_url=config_url_test[f"uuid{random.randint(1,2)}"])
            t_list.append(name)
        # time.sleep(20)
        else:
            name = bendi_video(uid, video=config_bendi[f"uuid{random.randint(1, 2)}"],
                               result_url=config_url_test[f"uuid{random.randint(1, 2)}"])
            t_list.append(name)

        if len(t_list) == 5:
            time.sleep(10)
            print(t_list)
            for i in reversed(range(random.randint(1, 4))):
                # print(random.randint(1,4))
                print(i)
                stop_video(t_list[i])
                print("停止了%s" % i)
                del t_list[i]

            time.sleep(5)
            print(t_list)
