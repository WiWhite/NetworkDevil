from getpass import getuser
from crontab import CronTab
import os


def add_cron(minute, hour, day):

    try:
        my_cron = CronTab(user=getuser())

        job = my_cron.new(command='python3 backup_master.py; python3 limit_files.py')
        job.minute.on(minute)
        job.hour.on(hour)
        job.dow.on(day)

        my_cron.write()

    except ValueError:
        my_cron = CronTab(user=getuser())

        job = my_cron.new(command='python3 backup_master.py; python3 limit_files.py')
        job.minute.on(minute)
        job.hour.on(hour)

        my_cron.write()


def update_cron(minute, hour, day):
    
    try:
        existing_cron = CronTab(user=getuser())
        for job in existing_cron:
            if job.command == 'python3 backup_master.py; python3 limit_files.py':
                job.minute.on(minute)
                job.hour.on(hour)
                job.dow.on(day)

                existing_cron.write()

    except ValueError:
        my_cron = CronTab(user=getuser())

        job = my_cron.new(command='python3 backup_master.py; python3 limit_files.py')
        job.minute.on(minute)
        job.hour.on(hour)

        my_cron.write()
