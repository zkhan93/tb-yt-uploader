#!/bin/sh
poetry run celery -A app.celery beat --loglevel=INFO
