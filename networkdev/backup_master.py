import paramiko
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networkdev.settings')
django.setup()

from editordb.models import Devices
import threading
import datetime


DEVICES = Devices.objects.all()


def ssh_connection(ip_address, login, password, production):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(
        ip_address,
        username=login,
        password=password
        )

    output = None
    timesleep = threading.Event()

    if production.production == 'cisco':

        terminal = client.invoke_shell()
        timesleep.wait(timeout=1)

        terminal.send('term len 0\n')
        timesleep.wait(timeout=1)

        terminal.send('terminal datadump\n')
        timesleep.wait(timeout=1)

        terminal.send('sh run\n')
        timesleep.wait(timeout=10)

        output = terminal.recv(99999)

    elif production.production == 'HP':

        terminal = client.invoke_shell()
        timesleep.wait(timeout=1)

        terminal.send('screen-length disable\n')
        timesleep.wait(timeout=1)

        terminal.send('display current-configuration\n')
        timesleep.wait(timeout=10)

        output = terminal.recv(99999)

    client.close()

    return output


def telnet_connection(device):
    pass


def backup_name(ip_address):

    now = datetime.datetime.now()
    filename = '{}_{}-{}-{}_{}-{}-{}.{}'.format(
                                        ip_address,
                                        now.day,
                                        now.month,
                                        now.year,
                                        (now.hour + 2),
                                        now.minute,
                                        now.second, 'cfg')
    return filename


def save(device, filename, output):

    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_with_backups = 'BACKUPS'
    devicedir = os.path.join(basedir, dir_with_backups, device.ip_address)

    if not os.path.exists(os.path.join(basedir, dir_with_backups)):
        os.makedirs(os.path.join(basedir, dir_with_backups))

    if not os.path.exists(devicedir):
        os.makedirs(devicedir)

    if device.location_backups == '':
        device.location_backups = devicedir
        device.save()

    with open('{}/{}'.format(devicedir, filename), 'wb') as f:
        f.write(output)


def main():

    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logfile = 'networkdev.log'
    pathlog = os.path.join(basedir, logfile)

    for device in DEVICES:

        now = datetime.datetime.now()
        time = '{}-{}-{}_{}-{}-{}'.format(
                                          now.day,
                                          now.month,
                                          now.year,
                                          (now.hour + 2),
                                          now.minute,
                                          now.second
                                          )

        try:
            config = ssh_connection(
                               device.ip_address,
                               device.login,
                               device.password,
                               device.production
                               )

            with open(pathlog, 'a') as f:
                done = '\n{}{}{}{}{}'.format(
                                    time,
                                    '---',
                                    device.ip_address,
                                    '---',
                                    'DONE'
                                    )
                f.write(done)

        except (paramiko.ssh_exception.NoValidConnectionsError, TimeoutError):
            with open(pathlog, 'a') as f:
                error = '\n{}{}{}{}{}'.format(
                                     time,
                                     '---',
                                     device.ip_address,
                                     '---',
                                     'ERROR'
                                     )
                f.write(error)
            continue

        name = backup_name(device.ip_address)
        save(device, name, config)


if __name__ == '__main__':

    main()
