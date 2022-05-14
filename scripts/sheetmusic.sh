apt-get update
apt-get -y install ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
mkdir tessdata
wget -O tessdata/tessdata_best.zip https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip --progress=dot:giga
unzip tessdata/tessdata_best.zip -d tessdata/
rm tessdata/tessdata_best.zip