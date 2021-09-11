# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=web.settings
WORKDIR /app
COPY site/requirements.txt .flake8 pyproject.toml /app/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr
RUN mkdir tessdata
RUN wget -O tessdata/tessdata_best.zip https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip
RUN unzip tessdata/tessdata_best.zip -d tessdata/
RUN rm tessdata/tessdata_best.zip
