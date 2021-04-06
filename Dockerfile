FROM python:3.9-alpine

WORKDIR /main

COPY ./ ./

RUN apk add py3-pip

RUN apk update

RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install -r requirements.txt

CMD python3 main.py