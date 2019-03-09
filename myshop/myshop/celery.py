#rabbitmqctl status
import os
from celery import Celery
from django.conf import settings

# 为celery程序设置环境为当前项目的环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


#celery -A myshop worker -l info
#celery -A myshop worker -l info -P eventlet