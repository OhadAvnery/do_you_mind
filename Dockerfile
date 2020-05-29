FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
COPY doyoumind doyoumind
COPY scripts/wait_for_it.sh wait_for_it.sh
RUN pip install -r requirements.txt