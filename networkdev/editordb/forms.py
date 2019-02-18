from django import forms

from .models import Devices, Crontab


class DevicesForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = ('ip_address',
                  'login',
                  'password',
                  'production',
                  'connection_type',)


class CrontabForm(forms.ModelForm):
    class Meta:
        model = Crontab
        fields = ('minute', 'hour', 'day', 'ttl_backups')
