#!flask/bin/python
from common import getFileBuff
from flask import Flask, request
from imei import imei
from IDCard import IDCard
from paddleocr import PaddleOCR
import numpy
import cv2
import traceback
import time
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

pocr = PaddleOCR(use_angle_cls=True, lang="ch")
gime = imei(pocr)
gidcard = IDCard(pocr)
debug_path = '../debug'
DEBUG=False


@app.route('/api/test',methods=['get'])
def do_test():
    return 'Hello World!'

@app.route('/api/ime', methods=['POST'])
def do_ime():
    """
    imei 号识别主入口，post  格式为
    {
        "img": "url 或者 图片base64"
    }
    :return:
    """
    parame_json = request.json
    err_json = {}
    if not "img" in parame_json.keys():
        err_json["error_code"] = 400
        err_json["error_msg"] = "img参数不存在"
        return err_json, 200
    img = parame_json["img"]
    try:
        image_buff = getFileBuff(img)
        str_encode = numpy.frombuffer(image_buff, numpy.uint8)
        image = cv2.imdecode(str_encode, cv2.IMREAD_COLOR)
        result = gime.run(image)
        lines = []
        for line in result:
            pos = [{"x": xy[0], "y": xy[1]} for xy in line[0]]
            line_json = {
                "word": line[1][0],
                "pos": pos
            }
            lines.append(line_json)
        re_json = {"prism_wordsInfo": lines}
    except Exception as e:
        err_json["error_code"] = 401
        err_json["error_msg"] = traceback.format_exc()
        return err_json
    return re_json


@app.route('/api/idcard/<side>', methods=['POST'])
def do_IDCard(side):
    """
    /api/idcard/face   正面检测
    /api/idcard/back    背面
    识别身分证正面信息，输入post格式 为
    {
        "img": "url 或者 图片base64"
    }
    :return:
    """
    run_map = {
        "face":gidcard.face,
        "back":gidcard.back
    }
    parame_json = request.json
    err_json = {}
    if not "img" in parame_json.keys():
        err_json["error_code"] = 400
        err_json["error_msg"] = "img参数不存在"
        return err_json, 200
    img = parame_json["img"]
    try:
        image_buff = getFileBuff(img)
        str_encode = numpy.frombuffer(image_buff, numpy.uint8)
        image = cv2.imdecode(str_encode, cv2.IMREAD_COLOR)
        filename = str(time.time())+'_'+side
        path = os.path.join(debug_path,time.strftime("%Y-%m", time.localtime()))
        if not os.path.exists(path):
            os.makedirs(path)
        cv2.imwrite(os.path.join(path,filename + ".jpg"),image)
        re_json = run_map[side](image)
        if len(re_json)>0:
            with open(os.path.join(path,filename + ".log"),'w',encoding="utf-8") as f:
                json.dump(re_json,f,ensure_ascii=False,indent=4)

    except Exception as e:
        err_json["error_code"] = 401
        err_json["error_msg"] = traceback.format_exc()
        return err_json
    return re_json


@app.route('/api/imei', methods=['POST'])
@app.route('/api/Mobile', methods=['POST'])
def do_imei():
    """
    imei 号识别主入口，post  格式为
    {
        "ImageInfo":"url 或者 图片base64",
        "Token":"111",
        "OrderId":"123456",
        "ClientId":"test"
    }
    :return:
    """
    re_json = {}
    try:
        parame_json = request.json
        img = parame_json["ImageInfo"]
        orderid=parame_json["OrderId"]
        image_buff = getFileBuff(img)
        str_encode = numpy.frombuffer(image_buff, numpy.uint8)
        image = cv2.imdecode(str_encode, cv2.IMREAD_COLOR)
        lret= gime.imei(image)
        re_json["code"]=0
        re_json["message"] = "请求成功"
        re_json["data"] = {"imei":lret}
        if DEBUG:
            filename = str(time.time()) + '_' + orderid
            path = os.path.join(debug_path, time.strftime("%Y-%m", time.localtime()))
            if not os.path.exists(path):
                os.makedirs(path)
            cv2.imwrite(os.path.join(path, filename + ".jpg"), image)
            if len(lret) > 0:
                with open(os.path.join(path, filename + ".log"), 'w', encoding="utf-8") as f:
                    json.dump(re_json, f, ensure_ascii=False, indent=4)
    except Exception as e:
        re_json["code"] = 500
        re_json["message"] = traceback.format_exc()

    return re_json,200


if __name__ == '__main__':
    app.run(debug=True)