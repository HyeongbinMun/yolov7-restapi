#!/usr/bin/env bash
CELERY_WORKER_QUEUES=WebAnalyzer celery -A AnalysisEngine worker --concurrency=1 --queues=WebAnalyzer --loglevel=info
