from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse

from .forms import DevicesForm
from .models import Devices


class DevicesView(View):

    def get(self, request):
        devices = Devices.objects.all()
        return render(request, 'editordb/index.html', {'devices': devices})


class AddDevice(View):

    def get(self, request):
        form = DevicesForm()
        return render(request, 'editordb/add_device.html', {'form': form})

    def post(sels, request):
        form = DevicesForm(request.POST)

        if form.is_valid():
            new_device = Devices(
                ip_address=form.cleaned_data['ip_address'],
                login=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                production=form.cleaned_data['production'],
                connection_type=form.cleaned_data['connection_type'],
            )
            new_device.save()
            return HttpResponseRedirect(reverse('devices_list_url'))
        else:
            return render(request, 'editordb/add_device.html', {'form': form})


class UpdateDevice(View):

    def get(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(instance=device)
        return render(request, 'editordb/update_device.html', {'form': form, 'device': device})

    def post(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(request.POST, instance=device)

        if form.is_valid():
            update_device = form.save()
            return HttpResponseRedirect(reverse('devices_list_url'))
        else:
            return render(request, 'editordb/update_device.html', {'form': form})


class DeleteDevice(View):

    def get(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(instance=device)
        return render(request, 'editordb/delete_device.html', {'device': device})

    def post(self, request, id):
        device = Devices.objects.get(pk=id)
        device.delete()
        return HttpResponseRedirect(reverse('devices_list_url'))
