# Set workdir to scripts/
cd "$(dirname "$0")/"

sh run.sh python site/manage.py test site/$@
