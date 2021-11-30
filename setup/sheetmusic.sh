apt-get update
apt-get -y install ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr
mkdir tessdata
wget -O tessdata/tessdata_best.zip https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip
unzip tessdata/tessdata_best.zip -d tessdata/
rm tessdata/tessdata_best.zip
