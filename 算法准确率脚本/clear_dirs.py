"""
   初始化删除之前项目遗留的文件
"""
import os
import shutil


path = os.path.abspath(os.path.dirname(__file__))

ori_dir = os.path.join(path, 'input')
ori_json = os.path.join(path, '.temp_files')

def clear():
    # 先清空文件夹 在创建文件夹
    if os.path.exists(ori_dir):
        shutil.rmtree(ori_dir)
    if os.path.exists(ori_json):
        shutil.rmtree(ori_json)

    # 创建需要的文件夹
    os.mkdir(ori_dir)
    detection_results = os.path.join(ori_dir, "detection-results")
    ground_truth = os.path.join(ori_dir, "ground-truth")
    os.makedirs(detection_results)
    os.makedirs(ground_truth)
# clear()