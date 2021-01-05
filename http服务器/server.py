#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import base64
import json
import uuid
from datetime import datetime

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        # random_name = ''.join([each for each in str(uuid.uuid1()).split('-')])
        image_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        with open('1.txt', 'wb') as f:
            f.write(self.data_string)
        obj = json.loads(self.data_string)
        res_base64 = obj.get("identifyPic")
        sysCode = obj.get("sysCode")
        ruleNo = obj.get("ruleNo")
        eqpNo = obj.get("eqpNo")
        image_name = sysCode + '_' + ruleNo + '_' + eqpNo + '_' + image_name
        if res_base64 is not None:
            res_image = base64.decodebytes(res_base64.encode('ascii'))
            print(f"res_image:{image_name}")
            with open(f'res_jpg/{image_name}.jpg', 'wb') as f:
                f.write(res_image)
        else:
            print("算法识别输出图片base64为空")

        ori_base64 = obj.get('rawPic')
        if ori_base64 is not None:
            ori_image = base64.decodebytes(ori_base64.encode('ascii'))
            print(f"ori_image:{image_name}")
            with open(f'ori_jpg/{image_name}.jpg', 'wb') as f:
                f.write(ori_image)
        else:
            print("输出原图base64为空")

        # print("-------------------------", self.data_string )

def run(server_class=HTTPServer, handler_class=S, port=8010):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
