import rarfile
import os
path = r'C:\Users\Administrator\Desktop\数据集\手绘识别训练数据'
path_1 = r'C:\Users\Administrator\Desktop\数据集\shouhui'

def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.rar')]

def un_rar(file_name):
    """unrar zip file"""
    print(file_name)
    for file in file_name:
        rf = rarfile.RarFile(file)
        rf.extractall(path_1) 
        print (file+'open')


if __name__ == '__main__':
    file = get_imlist(path)
    un_rar(file)