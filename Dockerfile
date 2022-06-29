FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y swig vim
RUN apt-get python3

COPY . .
RUN pip install -r requirements.txt


RUN chmod 777 /app
