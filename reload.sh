pkill gunicorn
rm gunicorn*
gunicorn --workers=8 --bind 0.0.0.0:5007 run:app --access-logfile gunicorn.log --error-logfile gunicorn-error.log --capture-output -D