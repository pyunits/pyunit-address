FROM alpine:3.12.0
MAINTAINER Jytoui <jtyoui@qq.com>

# 加入pip源
ENV pypi https://pypi.douban.com/simple

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装Python3环境
RUN apk add --no-cache python3 py-pip

# 更换pip3
RUN pip3 install --upgrade pip -i ${pypi}

# 安装flask插件
RUN pip3 install flask -i ${pypi}

ENV DIR /mnt/pyunit-address
COPY ./ ${DIR}
WORKDIR ${DIR}

# 安装项目第三方库
RUN pip3 install whl/uWSGI-2.0.18-cp38-cp38-linux_x86_64.whl
RUN pip3 install whl/pyahocorasick-1.4.0-cp38-cp38-linux_x86_64.whl
RUN pip3 install --no-cache-dir -r requirements.txt -i ${pypi}

RUN rm -rf whl

CMD ["sh","app.sh"]