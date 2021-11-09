# syntax=docker/dockerfile:1
FROM python:3.10.0
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app

# Then setup the rest
COPY requirements.txt /app/
RUN pip install -r requirements.txt
