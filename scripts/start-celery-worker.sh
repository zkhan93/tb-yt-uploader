#!/bin/sh
poetry run celery -A app.celery.worker worker --loglevel=DEBUG
