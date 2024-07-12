FROM python:3.11

WORKDIR /app

COPY functional/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt --no-cache-dir \
    && ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

COPY functional /app/functional
COPY .env /app/.env

ENV PYTHONPATH=/app

WORKDIR /app