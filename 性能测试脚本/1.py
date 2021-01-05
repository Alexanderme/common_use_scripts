import os

path = r'C:\Users\Administrator\Desktop\res\i3\i3_1\ev_uniform_gpu_sdk3.0_lic1b'

files = [file for file in os.listdir(path) if file.startswith('res')]

file_10 = []
file_0 = []

for file in files:
    num = int(file.split('_')[-1].split('.')[0])
    file = os.path.join(path, file)
    if num < 10:
        with open(file, 'r', encoding='utf-8') as f:
            a = f.readlines()[-1].strip().split(" 0,")[-1]
            print(a)

for file in files:
    num = int(file.split('_')[-1].split('.')[0])
    file = os.path.join(path, file)
    if num >= 10:
        with open(file, 'r', encoding='utf-8') as f:
            a = f.readlines()[-1].strip().split(" 0,")[-1]
            print(a)
