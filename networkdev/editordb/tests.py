import os
import django

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.path.join(basedir, 'networkdev.settings'))
django.setup()

print(os.path.join(basedir, 'networkdev/settings'))

from django.test import TestCase

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.core.paginator import Paginator



from .forms import DevicesForm, CrontabForm
from .models import Devices, Crontab


try:
    crontab = Crontab.objects.get()
except Crontab.DoesNotExist:
    crontab = None

form = CrontabForm(instance=crontab)
context = {'form': form, 'crontab': crontab}
templates = ['editordb/update_crontab.html', 'editordb/index.html']

print(crontab)
