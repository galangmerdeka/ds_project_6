FROM python:3.9.5-slim-buster

RUN apt-get update -y

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .