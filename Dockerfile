FROM  ubuntu:18.04
RUN sed -i s@/archive.ubuntu.com/@/mirrors.163.com/@g /etc/apt/sources.list && sed -i s@/security.ubuntu.com/@/mirrors.163.com/@g /etc/apt/sources.list && apt-get clean && apt update && apt -y install python3 python3-pip libxext6 libxrender1 libsm6
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y install tzdata
RUN echo "Asia/Shanghai" > /etc/timezone && rm -f /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --default-timeout=300 --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 8888
CMD ["uwsgi", "--ini=uwsgi.ini"]