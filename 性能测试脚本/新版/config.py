
# 测试服务器内存大小 M
MEMS_TOTAL = "free -m |awk 'NR==2 {print $2}'"
# 测试服务器显存大小 M
GPUS_TOTAL = "nvidia-smi |grep Default|awk 'NR==1 {print $11}'"
# 测试服务器核心
CPUS_TOTAL = "lscpu |grep CPU\(s\):|awk 'NR==1 {print $2}'"

# 获取当前运行的IAS进程
IAS_PID = "pidof ias"
# 获取当前算法的CPU占用
CPUS_USE = "top -n 1 -p %s|grep ias|awk '{print $9}'"
# 获取当前算法的内存占用
MEMS_USE = "top -n 1 -p %s|grep ias|awk '{print $9}'"
# 获取当前算法GPU占用
GPUS_USE = "nvidia-smi |grep %s |awk 'NR==1 {print $6}'"

# 算法启动方式  封装ias中使用 ias_package
ALGO_RUN = "docker run -itd --runtime=nvidia --privileged -e NVIDIA_VISIBLE_DEVICES=0 -v /tmp/ljx:/tmp -p %s:10000 --rm"
IAS_NAME_34 = "ias_3.4.tar.gz"
IAS_NAME_41 = "ias_4.1.tar.gz"
# 获取OPenCV版本
OPENCV_VERSION = "docker exec -it  %s  bash ldd /usr/local/ev_sdk/lib/libji.so |egrep  'libopencv_core.so.4'"
# 封装 IAS
IAS_PACKING = "cp ./ias_packages/%s /tmp/ljx;tar -xvf /tmp/ljx/%s -C /tmp/ljx"
# 授权
GIVE_AUTH = "docker exec  %s bash /tmp/give_license.sh &"
# 判断是否封装成功
IAS_IS_SUCESS = "docker exec %s bash -c 'cat /usr/local/ias/ias_data/log/ias.INFO|grep \"ji_init return = 0\"'"
# 获取本机IP
GET_LOCAL_IP = "ifconfig | grep inet | grep -v inet6 |grep  -F '192.168.1.'|awk '{print $2}'"


# 重启docker
RESTART_DOCKER = "systemctl restart docker"

# 图片存放目录
IMAGES = "./TestDatas/images"
# 视频存放目录
VIDEOS = "./TestDatas/videos"


# 算法启动时间等待算法稳定
SLEEP_TIME = 300
# 运行算法时长
FPS_TIME = 5000


# 保存结果文件夹
base_dir = "./res"
# 挂载目录文件夹
main_dir = "/ljx"
con_dir = "/ljx"

image_names = [("算法镜像", 1)]
