FROM python:3.7.0

MAINTAINER poppy

#RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories\
#    && apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community mariadb-dev libffi-dev
##    && ln -s /usr/include/locale.h /usr/include/xlocale.h

#定义环境变量
ENV TIME_ZONE Asia/Shanghai

ENV WECHATBOTENV 'local'

RUN apt install tzdata
#设置时区
RUN echo "${TIME_ZONE}" > /etc/timezone

RUN ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

#RUN  ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN mkdir /workspace

WORKDIR /workspace

COPY . /workspace

RUN pip install   -r /workspace/requirements.txt -i https://pypi.douban.com/simple/

#RUN python /workspace/setup.py install

COPY run.sh /run.sh

RUN chmod +x /run.sh

ENTRYPOINT [ "/run.sh","${e}" ]
