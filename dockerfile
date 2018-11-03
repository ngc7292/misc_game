# version: 0.0.1
FROM ubuntu:16.04
MAINTAINER ngc7293 "feizhaoye@gmail.com"

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN pip3 install numpy
RUN pip3 install -U wxpy -i "https://pypi.doubanio.com/simple/"


RUN mkdir /home/ngc7293

RUN useradd ngc7293 -d /home/ngc7293

RUN chmod 777 /home/ngc7293

USER ngc7293

WORKDIR /home/ngc7293

ADD server.py ./server.py
