FROM python:3.7-alpine

ENV TARHOSTING_STATIC_DIR /static
ENV TARHOSTING_TIMEOUT 30

RUN mkdir -p /usr/src/app/tarhosting
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY tarhosting /usr/src/app/tarhosting

EXPOSE 80

CMD gunicorn -b 0.0.0.0:80 -t $TARHOSTING_TIMEOUT --access-logfile - tarhosting.app:app
