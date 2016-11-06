FROM python:2.7-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
#RUN addgroup gunicorn && adduser gunicorn -D -G gunicorn gunicorn
COPY . /usr/src/app

#USER gunicorn
EXPOSE 80

CMD gunicorn -b 0.0.0.0:80 --access-logfile=/dev/stdout tarhosting.app:app
