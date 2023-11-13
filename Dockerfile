FROM python:3.9.6

WORKDIR /questionpro_flask

COPY . /questionpro_flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#COPY . .


# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]


# docker build -t questionpro_flask -f Dockerfile . --network=host

#docker run -d -p 5006:5000 questionpro_flask5:latest

#docker-compose up

# docker ps # to check the runing container

# docker stop