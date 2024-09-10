#!/bin/bash
# Kill celery worker
echo Killing Celery Worker
pkill -F .celery-worker.pid
# Kill celery beat
echo Killing Celery Beat
pkill -F .celery-beat.pid
# Remove pid files
rm .celery-worker.pid .celery-beat.pid
# Stop redis
echo Stopping Redis
killall redis-server
killall celery
# remove celerybeat-schedule file
rm celerybeat-schedule