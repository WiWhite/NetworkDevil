from getpass import getuser
from crontab import CronTab


def add_cron(minute, hour, day):

    try:
        my_cron = CronTab(user=getuser())

        command = 'python3 backup_master.py; python3 limit_files.py'
        job = my_cron.new(command=command)
        job.minute.on(minute)
        job.hour.on(hour)
        job.dow.on(day)

        my_cron.write()

    except ValueError:
        my_cron = CronTab(user=getuser())

        command = 'python3 backup_master.py; python3 limit_files.py'
        job = my_cron.new(command=command)
        job.minute.on(minute)
        job.hour.on(hour)

        my_cron.write()

cron = CronTab(user=getuser())

jobs = [el for el in cron]

print(jobs)

if jobs == []:
    print('false')
else:
    print('true')
