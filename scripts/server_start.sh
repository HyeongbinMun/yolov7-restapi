#!/usr/bin/env bash
nohup sh -- scripts/run_celery.sh > celery.log 2>&1 &
nohup sh -- scripts/run_django.sh > django.log 2>&1 &
echo "Start Server"
