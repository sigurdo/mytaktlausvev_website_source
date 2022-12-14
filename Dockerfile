# syntax=docker/dockerfile:1
FROM python:3.10.0

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings

WORKDIR /app

# Setup sheetmusic requirements first because it takes a long time and rarely changes.
# It's therefore important to be cached by Docker.
COPY scripts/sheetmusic.sh /app/
ARG SHEETMUSIC="yes"
RUN if [ $SHEETMUSIC = yes ]; then sh sheetmusic.sh; fi

# Download dependencies
COPY scripts/download_pdf_js.sh /app/
RUN ./download_pdf_js.sh

COPY site/requirements.txt /app/
RUN pip install --no-cache -r requirements.txt
