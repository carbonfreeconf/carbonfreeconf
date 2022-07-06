web: gunicorn conf.wsgi
main_worker: celery -A conf worker --beat --loglevel=info