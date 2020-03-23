FROM python:3.7-alpine
WORKDIR /opt/app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

RUN apk update && \
    apk add \
        linux-headers \
        libffi-dev musl-dev jpeg-dev zlib-dev freetype-dev \
        gcc \
        make \
        py3-pip \
        mysql-client

COPY requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# COPY docker-entrypoint.sh /opt/app/docker-entrypoint.sh
# RUN chmod +x /opt/app/docker-entrypoint.sh

ENTRYPOINT [ "/opt/app/docker-entrypoint.sh" ]