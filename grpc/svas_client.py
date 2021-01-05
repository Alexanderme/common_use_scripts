import os
import time

import grpc
import general_pb2
import general_pb2_grpc
from PIL import Image
from io import BytesIO
import random
from multiprocessing import Process, Pool

channel = grpc.insecure_channel('36.155.14.163:32720')
# channel = grpc.insecure_channel('192.168.1.147:11000')
stub = general_pb2_grpc.GeneralServiceStub(channel)
custom_data = general_pb2.CustomReqData(decoding_only_keyframes=False, callback_interval_s=0,
                                        whether_src_pic=False, whether_alarm_pic=True)

path = r"res_pic"


def request_generator(args_type):
    if args_type == "noargs":
        req = general_pb2.GeneralReq(stream_id="1234", stream_url="rtmp://58.200.131.2:1935/livetv/hunantv",
                                     custom_data=custom_data)
        yield req
    elif args_type == "roi":
        req = general_pb2.GeneralReq(stream_id="1235", stream_url="rtmp://58.200.131.2:1935/livetv/hunantv",
                                     args='{"roi":["POLYGON((0.4121212121212121 0.185,0.12121212121212122 0.815,0.9151515151515152 0.8625))"]}',
                                     custom_data=custom_data)
        yield req
    elif args_type == "noroi":
        req = general_pb2.GeneralReq(stream_id="1236", stream_url="rtmp://58.200.131.2:1935/livetv/hunantv",
                                     args='{"roi_fill":false, "draw_result":false}', custom_data=custom_data)
        yield req


def a(num, args):
    count = 0
    for responce in stub.General(request_iterator=request_generator(args)):
        print(responce.error_code)
        while responce.error_code == -3:
            a()
        if responce.alarm_pic_buffer:
            count += 1
            print(f"当前运行的算法路数{num}")
            bytes_stream = BytesIO(responce.alarm_pic_buffer)
            image = Image.open(bytes_stream)
            if not os.path.exists(r'res_pic_%s' % args):
                os.makedirs('res_pic_%s' % args)
            image.save(r'res_pic_%s\%s.jpg' % (args, count))


if __name__ == '__main__':
    pool = Pool(8)
    args = ["noargs", "roi", "noroi"]
    for i in range(4):
        pool.apply_async(func=a, args=(i, random.choice(args),))
    pool.close()
    pool.join()
    channel.close()
