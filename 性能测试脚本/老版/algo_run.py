import time
import os
import re
import sys
from config import Config


class Algo_run:
    """
    1:计算fps 2:计算启动数目用于x循环启动
    """

    def __init__(self):
        self.cpu_arry = []
        self.cpu_total_arry = []
        self.count_num = int(sys.argv[1])
        self.res_dir = sys.argv[2]
        self.run_method = sys.argv[3]
        start_time = time.time()
        os.chdir("/usr/local/ev_sdk/bin")
        os.system(self.run_method + " -r %s" % Config.fps_times)
        end_time = time.time()
        t = end_time - start_time
        res = round(t / Config.fps_times, 4)
        self.total_fps = float("%.2f" % (1 / res * int(self.count_num)))
        self.total_fps_time = int(1 / self.total_fps * 1000)
        self.each_fps = float("%.2f" % (1 / res))
        self.each_fps_time = int(1 / self.each_fps * 1000)

    def write_file(self, cpu_count, cpu_count_total):
        # test进程号
        pid_test = str(os.popen("pidof test").read().replace('\n', ""))
        pid_test_ji_api = str(os.popen("pidof test-ji-api").read().replace('\n', ""))
        if pid_test == "":
            pid_test = pid_test_ji_api
        if pid_test != "":
            # 总显存占用
            nvidia_count = int(
                os.popen("nvidia-smi |grep Default|awk '{print $9}'").read().split('M')[0].replace('\n', "").replace(
                    " ", ""))
            each_nvidia_count = int(nvidia_count / self.count_num)

            # 内存占用%
            mem_count = float(
                os.popen("top -n 1 -p %s |grep test  |awk '{print $11}'" % pid_test).read().replace('\n', "").replace(
                    " ", ""))
            mem_count_num = int(mem_count * Config.mem_total / 100)
            mem_count_total = mem_count_num * self.count_num

            # GPU温度
            nvidia_temp = str(
                os.popen("nvidia-smi |grep Default|awk '{print $3}'").read().replace('\n', "").replace(" ", ""))
            # cpu温度等于平均值
            cpu_temp = str(os.popen("sensors |grep Core|awk '{print $3}'").read().replace('\n', "").replace(" ", ""))

            temp_list = re.findall("(\d.\.\d)", cpu_temp)
            temp_avg = int(sum([float(s) for s in temp_list]) / 6)

            with open("%s/res_%s.txt" % (self.res_dir, self.count_num), "a") as q:
                q.write(f"内存占比={mem_count}%, MEM={mem_count_num}, 内存总占比={mem_count_total}, "
                        f"单个GPU占用(MB)={each_nvidia_count}, 总的GPU占用(MB)={nvidia_count}, GPU温度={nvidia_temp}, "
                        f"cpu={cpu_count}, 总cup占用={cpu_count_total}, CPU温度={temp_avg}, "
                        f"单路算法单帧分析耗时={self.each_fps_time}, 单路FPS={self.each_fps},"
                        f"当前服务器分析耗时={self.total_fps_time}, 当前服务器FPS={self.total_fps}")
                q.write("\n")
                q.write(f"{mem_count}%,{mem_count_num}, {mem_count_total}, {each_nvidia_count}, {nvidia_count},"
                        f" {nvidia_temp},{cpu_count}, {cpu_count_total}, {temp_avg}, {self.each_fps_time}, "
                        f"{self.each_fps}, {self.total_fps_time}, {self.total_fps}" + "\n")

    def get_cpu(self):
        # test进程号
        pid_test = str(os.popen("pidof test").read().replace('\n', ""))
        pid_test_ji_api = str(os.popen("pidof test-ji-api").read().replace('\n', ""))
        if pid_test == "":
            pid_test = pid_test_ji_api
        if pid_test != "":
            # cpu占用
            cpu_count = int(float(
                os.popen("top -n 1 -p %s |grep test  |awk '{print $10}'" % pid_test).read().replace('\n', "").replace(
                    " ", "")))
            #  总的cpu占用情况
            cpu_count_total = int(
                float(os.popen("top -n 3|grep Cpu  |awk '{print $2}'").read().replace('\n', " ").split(" ")[-2]))
            self.cpu_arry.append(cpu_count)
            self.cpu_total_arry.append(cpu_count_total)

    def get_use_info(self):
        export_path, run_sdk = self.run_method.split(";")
        print("%s;nohup %s -r 500000000  > run.log 2>&1 & " % (export_path, run_sdk))
        os.system("%s;nohup %s -r 500000000  > run.log 2>&1 & " % (export_path, run_sdk))
        time.sleep(10)
        # 每秒统计一次cpu占用
        for i in range(int(Config.sleep_time / 3)):
            self.get_cpu()
        cpu_total = sum(self.cpu_total_arry) / len(self.cpu_total_arry)
        cpu_total = int(cpu_total * Config.cpu_cores)
        max_cpu = max(self.cpu_arry)
        min_cpu = min(self.cpu_arry)
        cpu_count = str(min_cpu) + "%~" + str(max_cpu) + "%"
        cpu_count_total = str(cpu_total) + "%"
        self.write_file(cpu_count, cpu_count_total)


run = Algo_run()
run.get_use_info()
