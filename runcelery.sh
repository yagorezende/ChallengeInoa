#!/bin/bash
# Start celery worker
echo Starting Celery Worker
source .venv/bin/activate
source .env
# start redis
redis-server --daemonize yes
# start worker and save pid
celery -A challenge_inoa.celery worker --loglevel=info --detach --concurrency=10 --pidfile=.celery-worker.pid --logfile=.celery-worker.log
# Start celery beat
echo Starting Celery Beat
celery -A challenge_inoa.celery beat --loglevel=info --detach --pidfile=.celery-beat.pid --logfile=.celery-beat.log