"""
    #  @ModuleName: get_vedio_message
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/23 15:36
"""

import cv2


def video_message(file):
    cap = cv2.VideoCapture(file)
    # 帧率
    fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
    # 分辨率-宽度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 分辨率-高度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 总帧数
    frame_counter = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()
    # cv2.destroyAllWindows()
    # 时长，单位s
    # duration = frame_counter / fps

    return fps, frame_counter
