# -*- coding: utf-8 -*-
import os
from kombu import Queue
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnalysisEngine.settings')

BROKER_URL = 'amqp://mqadmin:mqpwdpwd@rabbitmq'
CELERY_RESULT_BACKEND = 'redis://yolov7-restapi_redis:6379/0'

app = Celery('AnalysisEngine', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.autodiscover_tasks(related_name='beats')

app.conf.update(
    accept_content=["json", "pickle"],
    task_serializer="json",
    result_serializer="pickle"
)
app.autodiscover_tasks()
app.conf.task_queues = (
    Queue('WebAnalyzer', 'WebAnalyzer', routing_key='webanalyzer_tasks'),
)
app.conf.timezone = 'Asia/Seoul'

app.conf.beat_schedule = {
    'delete_old_database': {
        'task': 'WebAnalyzer.tasks.delete_old_database',
        'schedule': timedelta(days=1),
        'args': (1,)
    },
}