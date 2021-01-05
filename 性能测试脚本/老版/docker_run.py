import os
from config import Config
import time


def run_docker(num, algo_dir, image_name, run_method):
    """
    启动容器, 运行算法脚本
    :param num: 给保存的txt文件加上标识数字
    :param algo_dir: 根据镜像名称和基础路径, 给每个算法文件夹命名
    :param image_name: 镜像名称
    :param record_time: 每个容器与需要记录的次数, 默认为1
    :return:
    """
    if not os.path.exists(algo_dir):
        os.makedirs(algo_dir)
    # 登录镜像仓库地址
    os.system("xxxxxxxxxxxxxxxxxxxxxx")
    # 启动容器 该部分操作需要在宿主机上面运行
    demo_docker = "docker run -itd --rm --runtime=nvidia --privileged -v %s:%s  -e LANG=C.UTF-8 -e " \
                  "NVIDIA_VISIBLE_DEVICES=all %s /bin/bash >%s/con_id.txt" % (
                      Config.main_dir, Config.con_dir, image_name, algo_dir)
    os.system(demo_docker)
    with open('%s/con_id.txt' % algo_dir, 'r') as f:
        docker_id = f.read()[0:6]
    # 需要的文件拷贝到容器 并且执行授权
    os.system("docker exec -it %s  bash %s/give_license.sh" % (docker_id, Config.main_dir))
    os.system('docker exec -it %s  python3 %s/algo_run.py %s %s "%s"' %
              (docker_id, Config.con_dir, num, algo_dir, run_method))


def count_dockers():
    # 在容器外运行 需要返回GPU算法能启动多少路
    num = 0
    # 获取当前启动的程序的个数 ./test 长度为6
    a1 = str(
        os.popen("nvidia-smi |grep vas|awk '{print $5}'").read().split('M')[0].replace('\n', "").replace(" ", ""))
    if len(a1) < 12:
        # 只需要在第一次启动时候计算本次总共可以启动多个算法
        a2 = str(
            os.popen("nvidia-smi |grep Default|awk '{print $9}'").read().split('M')[0].replace('\n', "").replace(
                " ",
                ""))
        a3 = str(
            os.popen("nvidia-smi |grep Default|awk '{print $11}'").read().split('M')[0].replace('\n', "").replace(
                " ",
                ""))
        # 获取当前GPU算法可以启动多少个
        try:
            num = int(a3) // int(a2)
            if num > 50:
                # 避免cpu算法 因为存在部分的机器占用显存导致启动路数太多
                num = 10
        except Exception as e:
            # 如果是cpu算法就默认启动10路算法  前提是内存够用
            print("CPU算法")
            num = 10
    return num


for image_dict in Config.image_names:
    image_name = image_dict[0]
    run_method = image_dict[1]
    run_file = image_dict[2]
    # 根据镜像名称, 给文件夹命名 默认为/ljx/res
    algo_dir = os.path.join(Config.base_dir, image_name.split("/")[-1].split(":")[0])
    print("---------------------------开始执行第一个容器---------------------------")
    run_docker(1, algo_dir, image_name, run_method)
    time.sleep(5)
    nums = count_dockers()
    for num in range(2, nums + 1):
        print("---------------------------总共{}个容器---------------------------".format(nums))
        print("---------------------------当前执行到{}个容器---------------------------".format(num))
        run_docker(num, algo_dir, image_name, run_method)
    os.system("systemctl restart docker")
    time.sleep(10)
