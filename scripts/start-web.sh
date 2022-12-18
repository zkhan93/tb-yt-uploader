#! /bin/sh
poetry run uvicorn app.web:app --host 0.0.0.0 --port 80 
