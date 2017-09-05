FROM python:3

RUN apt-get update         \
    && apt-get install -y  \
       unzip               \
    && apt-get clean

RUN wget https://www.digicert.com/CACerts/BaltimoreCyberTrustRoot.crt.pem \
    -qO /BaltimoreCyberTrustRoot.crt.pem

COPY . /app

RUN cd /app                            \
    && pip install -r requirements.txt

WORKDIR /app
CMD gunicorn -w 4 -b=0.0.0.0:80 wl.server:app
