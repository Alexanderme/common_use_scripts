import time
import os
from sdk_subprocess import sdk_subprocess
import config
from log import logger
from ias_package import IasPackage

class BaseResource:
    """
    初始化获取当前服务器资源信息
    """

    def __init__(self):
        self.gpu_total = config.GPUS_TOTAL
        self.mem_total = config.MEMS_TOTAL
        self.cpu_total = config.CPUS_TOTAL
        self.ip = os.popen(config.GET_LOCAL_IP).read().splitlines()[0]

    def get_cpus(self):
        status, cpus_total = sdk_subprocess(self.cpu_total)
        if not status:
            logger.error("获取当前服务器CPU核数失败 " + cpus_total)
        else:
            return cpus_total

    def get_mems(self):
        # 获取内存大小
        status, mems_total = sdk_subprocess(self.mem_total)
        if not status:
            logger.error("获取当前服务器MEM核数失败 " + mems_total)
        else:
            return mems_total

    def get_gpus(self):
        status, gpus_total = sdk_subprocess(self.gpu_total)
        if not status:
            logger.error("获取当前服务器GPU核数失败 " + gpus_total)
        else:
            return gpus_total


class BaseResourceUse(BaseResource):
    """
        基础类用来,实现共同需要获取的CPU使用和内存使用以及FPS
    """

    def __init__(self):
        super().__init__()
        self.ias_pids_cmd = config.IAS_PID
        self.cpus_total = super().get_cpus()
        self.gpus_total = super().get_gpus()
        self.mems_total = super().get_mems()
        self.cpu_use = config.CPUS_USE
        self.gpu_use = config.GPUS_USE
        self.mem_use = config.MEMS_USE

    def data_valid(self):
        if not self.cpus_total or not self.gpus_total or not self.mems_total:
            logger.error("获取当前服务器基本信息失败 ")
            exit(1)

    def get_ias_pid(self):
        status, ias_pids = sdk_subprocess(self.ias_pids_cmd)
        if not status:
            logger.error("获取当前服务器IAS进程ID失败 " + ias_pids)
        else:
            ias_pids = ias_pids.split(" ")
            return ias_pids

    def get_cpu_message(self, pid):
        status, cpu = sdk_subprocess(self.cpu_use % pid)
        if not status:
            logger.error("获取当前进程CPU使用失败 " + cpu)
        else:
            if cpu == "" or cpu is None:
                logger.error("获取当前进程CPU使用失败 ")
                exit(1)
            else:
                return cpu

    def get_mem_message(self, pid):
        status, mem = sdk_subprocess(self.mem_use % pid)
        if not status:
            logger.error("获取当前进程MEM使用失败" + mem)
        else:
            if mem == "" or mem is None:
                logger.error("获取当前进程MEM使用失败 ")
                exit(1)
            else:
                return mem

    def get_gpu_message(self, pid):
        status, gpu = sdk_subprocess(self.gpu_use % pid)
        if not status:
            logger.error("获取当前进程GPU使用失败 " + gpu)
        else:
            if gpu == "" or gpu is None:
                return None
            else:
                gpu = gpu[:-3]
                return gpu


class CpuAlgoResourceUse(BaseResourceUse):
    """
        cpu算法服务器资源占用
    """
    def get_gpu_counts(self):
        return int(self.cpus_total)


class GpuAlgoResourceUse(BaseResourceUse):
    """
        Gpu算法服务器启动路数
    """
    def __init__(self, image_name):
        super().__init__()
        self.time_to_count = False
        self.packing_ias = IasPackage(image_name)
        self.image_files = [os.path.join(config.IMAGES, file) for file in os.listdir(config.IMAGES)]

    def get_ias(self, port):
        # 获取服务器当前支持算法数目
        self.time_to_count = True
        from request_ias import requests_ias
        for i in range(50):
            for file in self.image_files:
                requests_ias(self.ip, port, file)

    async def get_gpu_counts(self):
        port = self.packing_ias.package_ias()[0]
        await self.get_ias(port)
        if self.time_to_count is True:
            time.sleep(150)
            gpu_use = self.get_gpu_message(self.get_ias_pid()[0])
            counts = int(int(self.gpus_total) / int(gpu_use))
            return counts

