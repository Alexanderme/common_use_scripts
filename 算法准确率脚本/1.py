"""
    #  @ModuleName: 1
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/9/3 11:09
"""
import os

# files = os.listdir("input/ground-truth")
files = os.listdir("input/detection-results")

for file in files:
    file = os.path.join('input/ground-truth', file)
    with open(file, 'r') as f:
        text = f.readlines()
    print(text)