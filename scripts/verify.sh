# Set workdir to scripts/
cd "$(dirname "$0")/"

sh lint.sh && sh test.sh
