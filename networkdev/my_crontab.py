import os
from getpass import getuser
from crontab import CronTab

basedir = os.path.dirname(os.path.abspath(__file__))


def add_cron(minute, hour, day):

    my_cron = CronTab(user=getuser())
    command = 'python3 {0}/backup_master.py; python3 {0}/limit_files.py'.format(basedir)

    try:

        list_my_cron = [jobs for jobs in my_cron]

        if list_my_cron == []:
            job = my_cron.new(command=command)
            job.minute.on(minute)
            job.hour.on(hour)
            job.dow.on(day)

            my_cron.write()

        else:
            for job in my_cron:
                if job.command == command:
                    job.minute.on(minute)
                    job.hour.on(hour)
                    job.dow.on(day)

                    my_cron.write()

    except ValueError:

        job.minute.on(minute)
        job.hour.on(hour)

        my_cron.write()
