FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

MAINTAINER Jytoui <jtyoui@qq.com>

COPY requirements.txt /app/requirements.txt

# 加入pip源
ENV pypi https://pypi.douban.com/simple

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装Python3环境
RUN apk add --no-cache --virtual mypacks \
            gcc  \
            python3-dev \
            linux-headers \
            musl-dev \
            && pip3 install --no-cache-dir -r /app/requirements.txt -i ${pypi} && \
            apk del mypacks

COPY ./pyunit_address /app/pyunit_address
COPY ./main.py /app/main.py