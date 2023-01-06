apt-get update
apt-get -y install poppler-utils tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
mkdir tessdata/tessdata_best-4.1.0
wget -P tessdata/tessdata_best-4.1.0 https://github.com/tesseract-ocr/tessdata_best/raw/4.1.0/nor.traineddata --progress=dot:mega
