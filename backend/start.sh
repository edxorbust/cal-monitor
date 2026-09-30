#!/bin/sh
set -eu
exec gunicorn calorie_tracker.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers "${WEB_CONCURRENCY:-2}" --threads 2 --timeout 60 --access-logfile - --error-logfile - --forwarded-allow-ips '*'
