FROM python:3

RUN apt-get update         \
    && apt-get install -y  \
       unzip               \
    && apt-get clean

COPY . /app

RUN cd /app                            \
    && pip install -r requirements.txt
