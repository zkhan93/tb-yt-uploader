#!/bin/sh
poetry run celery -A main.celery worker --loglevel=INFO --beat
