from getpass import getuser
from crontab import CronTab
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networkdev.settings')
django.setup()


def add_cron(minute, hour, day):

    my_cron = CronTab(user=getuser())

    job = my_cron.new(command='python3 backup_master.py')
    job.minute.on(minute)
    job.hour.on(hour)
    job.dow.on(day)

    my_cron.write()


def update_cron():
    pass
