# imeapi
手机imei号和身份证号码识别


# 编译
docker build -t ocr:v627 .

# 运行
docker run -d --rm -p 8888:8888 --name ocr ocr:v627

# postmain调用接口
## imei识别接口
post方法 <br>
 url:  ``` http://ip:8888/api/ime ``` <br>
body:
``` 
{
    "img": "url 或者 图片base64"
}
```
## 身份证识别接口
post方法 <br>
正面识别 url:  ``` http://ip:8888/idcard/face ``` <br>
背面识别 url:  ``` http://ip:8888/idcard/back ``` <br>
body:
``` 
{
    "img": "url 或者 图片base64"
}
```
