"""
    #  @ModuleName: sdk_docker_command
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/8/3 16:46
"""


#用于记录算法相关统一的配置
import argparse
from new_performance.libs import sdk_subprocess
# 创建解析步骤
args = argparse.ArgumentParser()

args.add_argument('-n', "--container_id", type=int, dest="", help='give cpus')
args.add_argument('-c', "--cpus", type=str, dest="cpus", help='give cpus')
args.add_argument('-i', "--image", type=str, dest="cpus", help='images_name')

args = args.parse_args()

volume_container_num = f"docker volume create vas-data{args.container_id}"

docker_command_41 = f' docker run -itd --privileged  -v opencv_41:/tmp  -e LANG=C.UTF-8 --cpuset-cpus="{args.cpus}" --rm {args.image}'

docker_command_34 = f' docker run -itd --privileged  -v opencv_34:/tmp  -e LANG=C.UTF-8 --cpuset-cpus="{args.cpus}" --rm {args.image}'

