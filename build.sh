#!/usr/bin/env bash


cd /pd/imeapi

docker build -t ocr:v627 .

#测试
docker run -d --rm -p 8888:8888 --name ocr ocr:v627

#推送
docker tag ocr:v627 docker.365xs.cn/community/ocr:v627
docker push docker.365xs.cn/community/ocr:v627


# 拉取
docker pull docker.365xs.cn/community/ocr:v627




#生产
docker stop ocr && docker rm ocr
docker run -d --restart=always  -p 8888:8888 --name ocr 192.168.3.36:10000/ocr:626