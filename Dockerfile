FROM python:2.7-alpine

ENV TARHOSTING_STATIC_DIR /static

RUN apk add --no-cache nginx-lua \
        supervisor

RUN mkdir -p /usr/src/app/tarhosting
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY tarhosting /usr/src/app/tarhosting

EXPOSE 80

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /run/nginx
RUN mkdir -p /etc/nginx/sites-enabled
COPY flask.conf /etc/nginx/nginx.conf
COPY supervisord.conf supervisord.conf

CMD ["/usr/bin/supervisord"]
