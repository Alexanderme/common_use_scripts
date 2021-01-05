"""
    #  @ModuleName: run_algo
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/8/1 11:30
"""
import os
import requests
from libs import sdk_subprocess, get_total_seconds
import subprocess
import uuid
import time

# 主目录绝对路径
path = os.path.dirname(os.path.abspath(__file__))


def get_opencv_num(image_name):
    """
    获取算法opencv版本
    :param image_name:
    :return:
    """
    flask_url_opencv = "http://192.168.1.147:5000/api/v1.0/sdk_opencv_message"
    data = {
        "image_name": image_name
    }
    res = requests.post(flask_url_opencv, data=data).json().get("errmsg")[-3:]
    return res


def run_sdk_opencv():
    """
    启动cpu算法命令创建算法基础环境
    :return:
    """
    cpu_total = "lscpu |grep CPU\(s\):|awk 'NR==1 {print $2}'"
    mem_total = "free -m |awk 'NR==2 {print $2}'"

    status, res_cpu_total = sdk_subprocess(cpu_total)
    if not status:
        print('res_cpu_total命令出现错误------------------')
        print(res_cpu_total)

    status, res_mem_total = sdk_subprocess(mem_total)
    if not status:
        print('res_mem_total命令出现错误------------------')
        print(res_mem_total)
    return res_cpu_total, res_mem_total


def number_test(sdk_num, cpuset_nums):
    total_nums = [cpuset_nums]
    for i in range(sdk_num):
        if int(sdk_num) == len(total_nums):
            return [sdk_num, total_nums]
        single_nums = []
        for s in total_nums[-1]:
            s += len(total_nums[-1])
            single_nums.append(s)
        total_nums.append(tuple(single_nums))


def cpunum_set(cpuset_nums):
    """
    主要用于cpu总个数计算共有多少个组合
    :param cpuset_nums:
    :return:
    """
    for cpu_num in cpuset_nums:
        cpuset_nums = []
        sdk_num, k = cpu_num
        for s in range(k):
            cpuset_nums.append(s)
        cpuset_nums = tuple(cpuset_nums)
        total_nums = [cpuset_nums]
        for i in range(sdk_num):
            if int(sdk_num) == len(total_nums):
                yield (sdk_num, total_nums)
            single_nums = []
            for s in total_nums[-1]:
                s += len(total_nums[-1])
                single_nums.append(s)
            total_nums.append(tuple(single_nums))


def docker_run(random_num, cpus, image, opencv_num):
    volume_container_num = f"docker volume create vas_{random_num}"
    status, res_volume_container_num = sdk_subprocess(volume_container_num)
    if not status:
        print('res_volume_container_num命令出现错误------------------', res_volume_container_num)
    vas_dir = "docker volume inspect  vas_%s|grep Mountpoint|awk '{print $2}'"%random_num
    status, res_vas_dir = sdk_subprocess(vas_dir)
    res_vas_dir = res_vas_dir[1:-8]
    opencv34_dir = "docker volume inspect  opencv_34 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv34_dir = sdk_subprocess(opencv34_dir)
    res_opencv34_dir = res_opencv34_dir[1:-8]
    opencv41_dir = "docker volume inspect  opencv_41 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv41_dir = sdk_subprocess(opencv41_dir)
    res_opencv41_dir = res_opencv41_dir[1:-8]
    if float(opencv_num) == 4.1:
        docker_command_41 = f' docker run -itd --privileged  -v {res_opencv41_dir}:/tmp  -v /data/vas_performance:/data -v vas_{random_num}:/usr/local/vas  --cpuset-cpus="{cpus}" --rm {image}'
        print(docker_command_41)
        status, res_docker_command_41 = sdk_subprocess(docker_command_41)
        if not status:
            print('res_docker_command_41命令出现错误------------------')
        print('res_docker_command_41', res_docker_command_41)
        docker_run_conf = f"cp {res_opencv41_dir}/run_3.0.conf {res_vas_dir}/run.conf"
        status, res_docker_run_conf = sdk_subprocess(docker_run_conf)
        if not status:
            print('docker_run_conf命令出现错误------------------')
        print('res_docker_run_conf', res_docker_run_conf)
        return res_docker_command_41
    else:
        docker_command_34 = f' docker run -itd --privileged  -v {res_opencv34_dir}:/tmp  -v  vas_{random_num}:/usr/local/vas -v /data/vas_performance:/data  --cpuset-cpus="{cpus}" --rm {image}'
        status, res_docker_command_34 = sdk_subprocess(docker_command_34)
        if not status:
            print('res_docker_command_34命令出现错误------------------')
        print(res_docker_command_34)
        docker_run_conf = f"cp {res_opencv34_dir}/run_2.5.conf {res_vas_dir}/run.conf"
        status, res_docker_run_conf = sdk_subprocess(docker_run_conf)
        if not status:
            print('docker_run_conf命令出现错误------------------')
        print(res_docker_run_conf)
        return res_docker_command_34

def get_performance_information(image_name):
    """
    运行算法得到算法占用信息
    :return:
    """
    res_cpu_total, res_mem_total = run_sdk_opencv()
    image_dir = image_name.split('/')[-1].split(":")[0]
    res_image_data = os.path.join(path, f'res_data')
    opencv_num = get_opencv_num(image_name)
    cpu_list = [(i, j) for i in range(1, 50) for j in range(2, 5) if i * j <= int(res_cpu_total)]
    opencv34_dir = "docker volume inspect  opencv_34 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv34_dir = sdk_subprocess(opencv34_dir)
    res_opencv34_dir = res_opencv34_dir[1:-8]
    opencv41_dir = "docker volume inspect  opencv_41 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv41_dir = sdk_subprocess(opencv41_dir)
    res_opencv41_dir = res_opencv41_dir[1:-8]

    for sdk_num, cpu_set_nums in cpunum_set(cpu_list):
        container_list = []
        for cpu_set_num in cpu_set_nums:
            print(sdk_num, cpu_set_num)
            random_num = ''.join([each for each in str(uuid.uuid1()).split('-')])
            #封装vas
            if float(opencv_num) == 3.4:
                docker_vas = f"docker build -t {image_name}_test --build-arg IMAGE_NAME={image_name} -f {res_opencv34_dir}/Dockerfile ."
            else:
                docker_vas = f"docker build -t {image_name}_test --build-arg IMAGE_NAME={image_name} -f {res_opencv41_dir}/Dockerfile ."
            status, res_docker_vas = sdk_subprocess(docker_vas)
            if not status:
                print('docker_vas命令出现错误------------------')
                print(res_docker_vas)
            image_name_test = image_name + "_test"
            cpuset_cpus = str(cpu_set_num).replace(" ", '')[1:-1]
            container_id = docker_run(random_num, cpuset_cpus, image_name_test, opencv_num)
            docker_auth = f"docker exec {container_id} bash /tmp/authorization.sh"
            subprocess.Popen(docker_auth, shell=True)
            # 等待算法运行300秒, 在统计资源占用
            time.sleep(10)
            container_id = container_id[:12]
            container_list.append(container_id)
            print("container_list", container_list)
        time.sleep(1700)
        for container_id, cpu_set_num  in zip(container_list,cpu_set_nums):
            cpuset_cpus = str(cpu_set_num).replace(" ", '')[1:-1]
            cpu_mem_used = "docker stats --no-stream |grep  %s |awk '{print $3$4}'" % container_id
            cpu_list = []
            mem_list = []
            for i in range(100):
                status, cpu_mem_used_res = sdk_subprocess(cpu_mem_used)
                time.sleep(1)
                if not status:
                    print('cpu_mem_used_res命令出现错误------------------')
                cpu_used, mem_used = cpu_mem_used_res.split('%')
                cpu_list.append(cpu_used)
                mem_list.append(mem_used[:-3])
            mem_used = max(mem_list)
            cpu_min = min(cpu_list)
            cpu_max = max(cpu_list)
            vas = f"/data/vas_performance/{container_id}/vas_data/log"
            vas_info = "ls %s |awk '{print $1}'" % vas
            info_log = os.popen(vas_info).read()
            vas_info = info_log.split('\n')[-3]
            fps,use_time, run_times  = get_total_seconds(os.path.join(vas, vas_info))
            with open(os.path.join(res_image_data, f'{image_dir}.txt'), 'a+', encoding='utf-8') as f:
                f.write(f"容器:{container_id}, 当前算法共运行路数:{sdk_num}, 当前指定CPU核数{cpuset_cpus}, 指定的CPU核数为:{len(cpu_set_num)}, 服务器总的CPU核数为{res_cpu_total}\n")
                f.write(f'当前算法cpu占用:{cpu_min}%~{cpu_max}%, 内存占用:{mem_used}MiB, 当前算法运行总时间:{use_time}S,运行总帧数:{run_times} FPS:{fps}\n')
            with open(os.path.join(res_image_data, f'{image_dir}_new.txt'), 'a+', encoding='utf-8') as f:
                f.write(f"{sdk_num} {cpuset_cpus} {len(cpu_set_num)} {mem_used} {cpu_min}%~{cpu_max}% {use_time} {run_times} {fps}\n\n")
        print("--------------------------------------------完成验证")
        os.system("systemctl restart docker")
images = ["算法镜像仓库地址"]
for image in images:
        get_performance_information(image)
