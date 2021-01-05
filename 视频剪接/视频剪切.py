import  os
import  sys
import shutil
from moviepy.editor import VideoFileClip




path = r'H:\算法\红色工作服\红色工作服数据\视频数据\原始视频\红色工服+安全帽\1'

#更换到视频路径
os.chdir(path)


# 创建文件夹
for i in range(1,11):
    try:
        os.mkdir(r"H:\算法\武警服装检测\徐栋\数据\视频数据\结果数据\%d"%i)
    except:
        pass



long = []
def get_files(path):
    return [os.path.join(path,file) for file in os.listdir(path) if file.endswith(".avi") or file.endswith(".mp4")]



files = get_files(path)
#获取视频时长
for file in files:
    clip = VideoFileClip(file)
    # print(clip.duration)
    s = int(clip.duration)
    long.append(s)


move_path = r"H:\算法\红色工作服\红色工作服数据\视频数据\原始视频\红色工服+安全帽\1"


file_num = 0
for video,time in zip(files,long):
    start_time_s = 0
    start_time_m= 0
    end_time_s = 0
    end_time_m = 0
    num = 0
    file_num = file_num + 1
    if time >5 :
        for i in range(int(time / 5)):
            num += 1
            if i == 0:
                end_time_s = end_time_s + 5
                os.system("ffmpeg  -i %s -vcodec copy -acodec copy -ss 00:%s:%s -to 00:%s:%s  %s_res.avi -y" % (video, str(start_time_m), str(start_time_s), str(end_time_m), str(end_time_s), str(num)))
            elif end_time_s < 55:
                start_time_s = end_time_s
                end_time_s = end_time_s + 5
                os.system("ffmpeg  -i %s -vcodec copy -acodec copy -ss 00:%s:%s -to 00:%s:%s  %s_res.avi -y" % (video, str(start_time_m), str(start_time_s), str(end_time_m), str(end_time_s), str(num)))
            elif end_time_s >= 55:
                start_time_s = end_time_s
                end_time_s = end_time_s + 5
                end_time_s = 0
                end_time_m = end_time_m + 1
                os.system("ffmpeg  -i %s -vcodec copy -acodec copy -ss 00:%s:%s -to 00:%s:%s  %s_res.avi -y" % (video, str(start_time_m), str(start_time_s), str(end_time_m), str(end_time_s), str(num)))
                start_time_m = start_time_m + 1

            shutil.move("%s_res.avi" % num, move_path + "\\" + str(file_num) + "\\" + "%s_res.avi" % num)


