import re
import os
from cv2 import cv2
from collections import defaultdict
import time
import requests
import shutil


# 1. 检查文件名称；  只包含因为数字下划线 并且以.jpg .mp4等结尾
# 2. 检查标注文件格式；txt  第一位int  后面属于0-1(归一化坐标)
# 3. 检查视频文件是否能正常打开；使用一个算法运行视频
# 4. 检查视频文件是否都是如标注时设定的一样，按照6帧每秒的方式标注。
# 5. 统计下 视频文件和标注文件个数是否一致


def check_filename(file):
    """
    检查文件名称；  只包含因为数字下划线 并且以.jpg .mp4等结尾
    :param file:   接收文件名称不包含路径
    :return:       返回命名错误的文件列表
    """
    file_addr_stand = ['jpg', 'png', 'jpeg', 'mp4', 'avi', 'txt', 'xml']
    filename_stand = re.compile('^[A-Za-z0-9_]*$')
    try:
        filename, file_addr = file.split('.')
        if not re.match(filename_stand, filename):
            return False
        if file_addr not in file_addr_stand:
            return False
    except:
        # 存在多个....
        return False
    return True


file_wrong_txt = defaultdict(int)
move_wrong_txt = defaultdict(list)

def check_tagging_datas(file, root):
    """
    用来检查txt标注结果是否正确
    :param file: 接收标注文件
    :return: 返回错误的标注文件
    """
    # 切割存在多个空格
    space_split = re.compile(r'[\s]\s*')
    if file.endswith('txt'):
        # txt  第一位int  后面属于0-1
        abs_filename = os.path.join(root, file).replace("\\", '/')
        with open(abs_filename, 'r', encoding='utf-8') as f:
            res_contents = f.read().splitlines()
            if res_contents == []:
                file_wrong_txt['space_txt'] += 1
                move_wrong_txt['space_txt'].append(abs_filename)
                return False
            for res_content in res_contents:
                datas = re.split(space_split, res_content)
                for i in range(len(datas)):
                    if not datas[0].isdigit():
                        return False
                    if i > 0:
                        if float(datas[i]) < 0:
                            file_wrong_txt['lager_one'] += 1
                            move_wrong_txt['lager_one'].append(abs_filename)
                            return False
                        if float(datas[i]) > 1:
                            file_wrong_txt['lager_one'] += 1
                            move_wrong_txt['lager_one'].append(abs_filename)
                            return False

        return True

def deal_wrong_file():
    # 移动txt
    for abs_filename in move_wrong_txt['space_txt']:
        dst = r'G:\数据\q3\fall\wrong\space'
        video_root, file = abs_filename.split('_label/')
        root, file = abs_filename.split('_label/')
        shutil.move(abs_filename, os.path.join(dst, file))
        # 移动视频
        video_file = file.split('.')[0] + '.mp4'
        shutil.move(os.path.join(video_root, video_file), os.path.join(dst, video_file))
    #处理大于1的txt
    for abs_filename in move_wrong_txt['lager_one']:
        deal_res = []
        with open(abs_filename, 'r', encoding='utf-8') as f:
            res_contents = f.read().splitlines()
            pattern = re.compile(' (1.\d\d\d)')
            for res_content in res_contents:
                res = re.sub(pattern, " 1.000", res_content)
                deal_res.append(res)
        with open(abs_filename, 'w', encoding='utf-8') as f:
            for deal in deal_res:
                f.write(deal+'\n')





def check_frame(abs_filename):
    """
    检查视频每秒是否是6帧
    :param abs_filename:
    :return:
    """
    try:
        cap = cv2.VideoCapture(abs_filename)
        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if int(fps) != 6:
            return False
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        return False
    return True


url = "http://192.168.1.147:60002/api/analysisVideo"
wrong_video = []


def run_video(file, abs_filename):
    """
    使用算法查看视频是否正常输出结果
    :param file:
    :param abs_filename:
    :return:
    """
    data = {
        'video': (file, open(abs_filename, 'rb'))
    }
    try:
        res_image = requests.post(url, files=data)
        if res_image.json().get("code") == -1:
            print("------------------算法未授权, 退出-----------------")
            print(abs_filename)
    except Exception as e:
        print("报错的图片{}".format(abs_filename))
        wrong_video.append(file)
        time.sleep(10)
        return None


path = 'G:/数据/q3/fall_v2/fall/'
file_count = defaultdict(int)
file_name = defaultdict(list)


def iter_files(rootDir):
    # 统计下 视频文件和标注文件个数是否一致

    for root, dirs, files in os.walk(rootDir):
        for file in files:
            abs_filename = os.path.join(root, file).replace("\\", '/')
            # 调用函数检查文件命名
            fileanme_res = check_filename(file)
            if not fileanme_res:
                print(abs_filename)
            # 查看txt结果
            if file.lower().endswith('txt'):
                file_count['tag_file'] += 1
                ignore_suffix_filename = file.split('.')[0]
                file_name['tag_file'].append(ignore_suffix_filename)
                tagging_res = check_tagging_datas(file, root)
                if not tagging_res:
                    print(abs_filename)
            # 检查视频帧数
            if file.lower().endswith('mp4') or file.lower().endswith('avi') or file.lower().endswith('flv'):
                file_count['video_file'] += 1
                ignore_suffix_filename = file.split('.')[0]
                file_name['video_file'].append(ignore_suffix_filename)
                video_frame = check_frame(abs_filename)
                if not video_frame:
                    print(abs_filename)
                # 运行视频查看视频是否正常运行
                run_video(file, abs_filename)
        for dir in dirs:
            iter_files(dir)


iter_files(path)
deal_wrong_file()
print(file_count)
print(file_wrong_txt)
print(move_wrong_txt)
# 如果两种文件总数不一致 输出结果
video_names = set(file_name['video_file'])
tag_names = set(file_name['tag_file'])
print(video_names - tag_names)

video_names = set(file_name['video_file'])
tag_names = set(file_name['tag_file'])
print(tag_names - video_names)
