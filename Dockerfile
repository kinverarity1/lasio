FROM python:3
MAINTAINER Kent Inverarity "kinverarity@hotmail.com"

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install --trusted-host pypi.python.org -r optional-packages.txt
RUN python setup.py install