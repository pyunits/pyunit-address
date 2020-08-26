FROM alpine:3.12.0
MAINTAINER Jytoui <jtyoui@qq.com>

# 加入pip源
ENV pypi https://pypi.douban.com/simple

EXPOSE 5000

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装Python3环境
RUN apk add --no-cache python3

COPY requirements.txt requirements.txt

# 安装Python3环境
RUN apk add --no-cache --virtual mypacks \
            gcc  \
            python3-dev \
            linux-headers \
            musl-dev \
            py-pip \
            && pip3 install --no-cache-dir -r requirements.txt uWSGI flask -i ${pypi} && \
            apk del mypacks

ENV DIR /mnt/pyunit-address
COPY ./ ${DIR}
WORKDIR ${DIR}

CMD ["sh","app.sh"]