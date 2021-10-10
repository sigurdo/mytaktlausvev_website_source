# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app
COPY site/requirements.txt .flake8 pyproject.toml /app/
RUN pip install -r requirements.txt
