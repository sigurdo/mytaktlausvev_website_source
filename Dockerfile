# syntax=docker/dockerfile:1
FROM python:3.10.0
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app

# Setup sheetmusic requirements first because it takes long time, changes rarely
# and is therefore important to be cached by docker.
COPY setup/sheetmusic.sh /app/
ARG SHEETMUSIC="yes"
RUN if [ $SHEETMUSIC = yes ]; then sh sheetmusic.sh; fi

# Then setup the rest
COPY site/requirements.txt .flake8 pyproject.toml /app/
RUN pip install --no-cache -r requirements.txt
