FROM python:3.9-alpine

WORKDIR /main

COPY ./ ./

RUN apk add py3-pip

RUN apk add alpine-sdk

RUN pip3 install -r requirements.txt

CMD uvicorn app:app --reload --host 0.0.0.0