FROM public.ecr.aws/bitnami/python:3.8.13-debian-11-r1

WORKDIR /app

RUN apt-get update && apt-get install -y swig vim

COPY . .
RUN pip install -r requirements.txt


RUN chmod 777 /app
