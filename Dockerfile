FROM public.ecr.aws/sam/build-python3.8:1.53.0-20220629192010

WORKDIR /app

RUN apt-get update && apt-get install -y swig vim

COPY . .
RUN pip install -r requirements.txt


RUN chmod 777 /app
