FROM python:3.8.6-buster

COPY api /api
COPY models /models
COPY requirements.txt /requirements.txt
COPY Makefile /Makefile
COPY hooked-on-recruiting-f6ef402ba1dc.json /credentials.json

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
