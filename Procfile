release: python manage.py migrate
web: bin/start-pgbouncer gunicorn config.asgi:application -k uvicorn_worker.UvicornWorker
worker: bin/start-pgbouncer REMAP_SIGTERM=SIGQUIT celery -A config.celery_app worker --loglevel=info
beat: bin/start-pgbouncer REMAP_SIGTERM=SIGQUIT celery -A config.celery_app beat --loglevel=info
