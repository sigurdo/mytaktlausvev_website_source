# syntax=docker/dockerfile:1
FROM python:3.9
ARG SHEETMUSIC="no"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app
COPY site/requirements.txt .flake8 pyproject.toml /app/
RUN pip install -r requirements.txt
RUN if [ $SHEETMUSIC = yes ]; then apt-get update; fi
RUN if [ $SHEETMUSIC = yes ]; then apt-get -y install ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr; fi
RUN if [ $SHEETMUSIC = yes ]; then mkdir tessdata; fi
RUN if [ $SHEETMUSIC = yes ]; then wget -O tessdata/tessdata_best.zip https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip; fi
RUN if [ $SHEETMUSIC = yes ]; then unzip tessdata/tessdata_best.zip -d tessdata/; fi
RUN if [ $SHEETMUSIC = yes ]; then rm tessdata/tessdata_best.zip; fi
