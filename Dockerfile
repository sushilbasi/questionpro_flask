FROM ubuntu:22.04
MAINTAINER basisushil@gmail.com

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY questionpro_flask /opt/

RUN pip3 install -r requirments.txt
WORKDIR /opt/


CMD ["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]


# docker build -t questionpro_flask -f Dockerfile . --network=host

#docker run -d -p 5006:5000 questionpro_flask5:latest

#docker-compose up

# docker ps # to check the runing container

# docker stop