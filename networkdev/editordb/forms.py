from django import forms

from .models import Devices


class DevicesForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = ('ip_address',
                  'login',
                  'password',
                  'production',
                  'connection_type',)
