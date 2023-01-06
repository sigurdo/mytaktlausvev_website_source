echo Migrating database
python site/manage.py migrate

echo Collecting static files
python site/manage.py generate_code_styles site/static/scss default monokai
python site/manage.py compilescss
python site/manage.py collectstatic --no-input

echo Starting Gunicorn
gunicorn web.wsgi:application --bind 0.0.0.0:8000 --chdir site
