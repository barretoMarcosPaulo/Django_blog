FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapps
WORKDIR /webapps
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip3 install -U pip setuptools
COPY requirements.txt /webapps/
RUN pip3 install -r /webapps/requirements.txt
ADD . /webapps/
EXPOSE 8000