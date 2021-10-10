# syntax=docker/dockerfile:1
FROM python:3.9
ARG SHEETMUSIC="no"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app
COPY site/requirements.txt .flake8 pyproject.toml setup/sheetmusic.sh /app/
RUN pip install -r requirements.txt
RUN if [ $SHEETMUSIC = yes ]; then sh sheetmusic.sh; fi
