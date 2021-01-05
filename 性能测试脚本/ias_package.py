"""
    #  @ModuleName: ias_packages
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/22 16:54
"""
import subprocess

from sdk_subprocess import sdk_subprocess
import config
from log import logger
import random
import time


class IasPackage:

    def __init__(self, image_name):
        # 用于判断 运行图片还是视频
        self.ports = []
        self.image_name = image_name

    def get_opencv_versiopn(self):
        self.port = random.randint(10000, 65000)
        self.ports.append(self.port)
        cmd_run_sdk = config.ALGO_RUN % self.port + f"{self.image_name}"
        status, res = sdk_subprocess(cmd_run_sdk)
        if not status:
            logger.error("启动算法失败 " + res)
            exit(1)
        contain_id = res[:12]
        opencv_message = config.OPENCV_VERSION % contain_id
        status, opencv_message = sdk_subprocess(opencv_message)
        if opencv_message is not '':
            opencv_message = 4.1
        else:
            opencv_message = 3.4

        return opencv_message, contain_id

    def package_ias(self):
        OpenCv, contain_id = self.get_opencv_versiopn()

        if OpenCv == 3.4:
            cmd = config.IAS_PACKING % (config.IAS_NAME_34, config.IAS_NAME_34)
            status, res = sdk_subprocess(cmd)
            if not status:
                logger.error("封装IAS失败 " + res)
                exit(1)
        else:
            cmd = config.IAS_PACKING % (config.IAS_NAME_41, config.IAS_NAME_41)
            status, res = sdk_subprocess(cmd)
            if not status:
                logger.error("封装IAS失败 " + res)
                exit(1)

            # 上传成功之后解压 安装
        ias_install = config.GIVE_AUTH % contain_id
        subprocess.Popen(ias_install, shell=True)
        time.sleep(10)
        cmd = config.IAS_IS_SUCESS
        status, res_code = sdk_subprocess(cmd)
        if not status or int(res_code[-1]) != 0:
            logger.error("封装IAS失败 " + res)
            exit(1)
        return self.ports

