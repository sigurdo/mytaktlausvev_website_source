#!/bin/sh
set -e               # Exit on error
cd /app/             # Set working directory to /app/

mkdir downloads
mkdir downloads/static
mkdir downloads/static/js

# pdf.js
mkdir downloads/static/js/pdf.js
cd downloads/static/js/pdf.js
wget -O pdf.js.zip https://github.com/mozilla/pdf.js/releases/download/v2.16.105/pdfjs-2.16.105-dist.zip --progress=dot:giga
unzip pdf.js.zip
rm pdf.js.zip
