#!/usr/bin/env bash



docker build -t ocr:v627 .

#测试
docker run -d --rm -p 8888:8888 --name ocr ocr:v627

