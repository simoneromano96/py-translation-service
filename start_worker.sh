#!/bin/sh

celery -A worker worker --loglevel=INFO --concurrency=1
