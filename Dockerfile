FROM python:3.6-alpine

MAINTAINER Adam Garibay <adam.garibay@gmail.com>

RUN mkdir /app

RUN pip install bs4 reqeusts

CMD python -u /app/app.py
