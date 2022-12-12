FROM python:3.9
LABEL maintainer="abhilash"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG CONFIG_PATH
ENV CONFIG_PATH $CONFIG_PATH

RUN apt-get update &&  apt-get install -y supervisor build-essential gcc libc-dev libffi-dev default-libmysqlclient-dev libpq-dev
RUN apt update && apt install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code

RUN rm -rf venv

RUN chmod +x docker-entry.sh

CMD ["./docker-entry.sh"]
