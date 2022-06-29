FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y swig vim

COPY . .
RUN pip install -r requirements.txt


RUN chmod 777 /app
