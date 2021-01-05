"""
    #  @ModuleName: config
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/8/1 12:23
"""

import subprocess
import datetime


def sdk_subprocess(cmd):
    """
    封装 subprocess 用来定制化返回消息
    :param cmd:
    :param msg:
    :return:
    """
    res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = res_p.communicate()
    returncode = res_p.returncode
    if returncode == 0:
        if stdout.endswith('\n'):
            return True, stdout.replace('\n', '')
        return True, stdout
    else:
        return False, stderr


def get_total_seconds(info_log):
    begin_time = "cat %s |grep event |awk '{print $2}' |head -1" % info_log
    print("begin_time%s"%begin_time)
    status, begin_time = sdk_subprocess(begin_time)
    if not status:
        print(f"begin_time:{begin_time}错误")
    end_time = "tac %s |grep event |awk '{print $2}'|head -1" % info_log
    status, end_time = sdk_subprocess(end_time)
    if not status:
        print(f"end_time:{end_time}错误")

    run_times = f"cat {info_log} |grep event |wc -l"
    status, run_times = sdk_subprocess(run_times)
    if not status:
        print(f"run_times:{run_times}错误")

    begin_time = datetime.datetime.strptime(begin_time, '%H:%M:%S.%f')
    end_time = datetime.datetime.strptime(end_time, '%H:%M:%S.%f')
    use_time = (end_time - begin_time).seconds

    fps = int(run_times) / int(use_time)
    return fps, use_time, run_times

