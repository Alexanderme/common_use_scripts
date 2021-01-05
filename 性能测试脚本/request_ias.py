"""
    #  @ModuleName: request_ias
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/23 14:28
"""
import requests
from log import logger
import time


def requests_ias(ip, port, files, counts):
    if files.endswith("jpg"):
        url = "http://" + str(ip) + ":" + str(port) + "/api/analysisImage"
        s = time.time()
        request_sample(url, files, counts, file_type="图片", )
        u = time.time()
        u = u - s
        return int(len(files)*counts/int(u))

    if files.endswith("avi"):
        url = "http://" + str(ip) + ":" + str(port) + "/api/analysisVideo"
        s = time.time()
        request_sample(url, files, counts, file_type="视频", )
        u = time.time()
        u = u - s
        return int(len(files)*counts/int(u))


def request_sample(url, files, counts, file_type):
    for i in range(counts):
        for file in files:
            with open(file, "rb") as f:
                fb = f.read()
            data = {
                "image": fb,
            }
            status_code = requests.post(url, files=data).json().get("code")
            if status_code != 0:
                logger.error(f"算法调用失败----{file_type}")
