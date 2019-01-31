from paramiko import SSHClient, AutoAddPolicy
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networkdev.settings')
django.setup()

from editordb.models import Devices
from time import sleep
import datetime




DEVICES = Devices.objects.all()

def ssh_connection(ip_address, login, password):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    client.connect(
        ip_address,
        username=login,
        password=password
        )

    terminal = client.invoke_shell()
    sleep(1)

    terminal.send('terminal datadump\n')
    sleep(1)

    terminal.send('sh run\n')
    sleep(10)

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
                                        now.hour,
                                        now.minute,
                                        now.second, 'cfg')
    return filename


def save(ip_address, location_backups, filename, output):

    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_with_backups = 'BACKUPS'
    devicedir = os.path.join(basedir, dir_with_backups, ip_address)

    if not os.path.exists(os.path.join(basedir, dir_with_backups)):
        os.makedirs(os.path.join(basedir, dir_with_backups))

    if not os.path.exists(devicedir):
        os.makedirs(devicedir)

    with open('{}/{}'.format(devicedir, filename), 'wb') as f:
        f.write(output)

    if location_backups == '':
        location_backups = devicedir
        location_backups.save()


def main():

    for device in DEVICES:
        config = ssh_connection(device.ip_address, device.login, device.password)
        name = backup_name(device.ip_address)
        save(device.ip_address, device.location_backups, name, config)


if __name__ == '__main__':

    main()
