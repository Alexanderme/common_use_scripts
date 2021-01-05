# encoding:utf-8
import os
import random
import string


path = r'C:\Users\Administrator\Desktop\streetbusiness\slr-4e4s0tmf\capture'

# 递归命名所有文件夹下面所有文件


def iter_files(rootDir):
    for root, dirs, files in os.walk(rootDir):
        count = 1
        data = root.split("\\")[-1]
        for file in files:
            os.rename(os.path.join(root, file), os.path.join(root, '%d.jpg') % (count))
            count += 1
        for dir in dirs:
            iter_files(dir)


iter_files(path)
