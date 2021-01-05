"""
    #  @ModuleName: AlgoRun
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/22 12:17
"""
from log import logger
from AlgoResourceUse import CpuAlgoResourceUse, GpuAlgoResourceUse
from ias_package import IasPackage
from request_ias import requests_ias
import os
import config
from multiprocessing import Pool
import time

image_files = [os.path.join(config.IMAGES, file) for file in os.listdir(config.IMAGES)]
video_files = [os.path.join(config.VIDEOS, file) for file in os.listdir(config.VIDEOS)]


class RecordFps:
    def __init__(self, image_name, count):
        self.image_name = image_name
        self.count = count
        self.ports = []

    def run_iass(self):
        """
        启动全部的ias
        :return:
        """
        for _ in range(self.count+1):
            ias = IasPackage(self.image_name)
            ports = ias.package_ias()
            self.ports = ports
        return self.ports

    def get_fps(self):
        pass

    def get_fps_total(self):
        pass

    def record_all_message(self):
        pass


if __name__ == "__main__":
    ports = []
    #  cpu_or_gou 1 cpu, file 1 pic
    image_name, cpu_or_gou, file_type = ("算法镜像", 1, 1)
    if cpu_or_gou == 1 and file_type == 1:
        "cpu算法"
        cpu_algo = CpuAlgoResourceUse()
        cpu_algo_nums = cpu_algo.get_gpu_counts()
        ip = cpu_algo.ip
        # 封装好全部的ias
        for i in range(cpu_algo_nums):
            ias_pack = RecordFps(image_name, i)
            ports = ias_pack.run_iass()
            # 调用
            # 获取当前并发数
            po = Pool(processes=len(ports))
            s = time.time()
            jobs = []
            for port in ports:
                jobs.append(po.apply_async(requests_ias, (ip, port, image_files, 500)))
            po.close()
            time.sleep(600)
            pids = cpu_algo.get_ias_pid()
            for pid in pids:
                cpu_message = cpu_algo.get_cpu_message(pid)
                mem_message = cpu_algo.get_mem_message(pid)
                f.write(cpu_message)
                f.write(mem_message)
            po.join()
            for res in jobs:
                with open('res.txt', 'a') as f:
                    f.write(str(res) + '\n')
                    f.write(res.get())
            os.system(config.RESTART_DOCKER)


    # elif cpu_or_gou == 1 and file_type != 1:
    #     "cpu算法"
    #     cpu_algo = CpuAlgoResourceUse()
    #     cpu_algo_nums = cpu_algo.get_gpu_counts()
    #     ip = cpu_algo.ip
    #     for i in range(cpu_algo_nums):
    #         ias = IasPackage(image_name)
    #         # 获取到全部的端口
    #         ports = ias.package_ias()
    #     for i in range(1, len(ports) + 1):
    #         ways = len(ports[:i])
    #         po = Pool(ways)
    #         for _ in range(100):
    #             for file in image_files:
    #                 requests_ias(ip, ports, file)
    else:
        gpu_algo = GpuAlgoResourceUse(image_name)
        gpu_algo.get_gpu_counts()
