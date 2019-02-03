from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DevicesForm, CrontabForm
from .models import Devices, Crontab

from my_crontab import add_cron
from diff_backups import show_diff


class DevicesView(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request):

        search_device = request.GET.get('search', '')

        if search_device:
            devices = Devices.objects.filter(ip_address=search_device)
        else:
            devices = Devices.objects.all()

        paginator = Paginator(devices, 10)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        try:
            crontab = Crontab.objects.get()
        except Crontab.DoesNotExist:
            crontab = None

        context = {
            'devices': page,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
            'crontab': crontab,
        }

        return render(request, 'editordb/index.html', context=context)


class AddDevice(LoginRequiredMixin, View):

    raise_exception = True

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


class UpdateDevice(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(instance=device)
        context = {
            'form': form,
            'device': device
            }
        return render(request, 'editordb/update_device.html', context=context)

    def post(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(request.POST, instance=device)
        templates = 'editordb/update_device.html'

        if form.is_valid():
            update_device = form.save()
            return HttpResponseRedirect(reverse('devices_list_url'))
        else:
            return render(request, templates, {'form': form})


class DeleteDevice(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request, id):
        device = Devices.objects.get(pk=id)
        form = DevicesForm(instance=device)
        templates = 'editordb/delete_device.html'
        return render(request, templates, {'device': device})

    def post(self, request, id):
        device = Devices.objects.get(pk=id)
        device.delete()
        return HttpResponseRedirect(reverse('devices_list_url'))


class DiffDevice(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request, id):
        device = Devices.objects.get(pk=id)
        if device.location_backups == '':
            diff = 'Diff for {} not available!'.format(device.ip_address)
        else:
            diff = show_diff(device.location_backups)
        return render(request, 'editordb/diff_backups.html', {'diff': diff})


class AddCrontab(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request):
        form = CrontabForm()
        return render(request, 'editordb/add_crontab.html', {'form': form})

    def post(self, request):
        form = CrontabForm(request.POST)

        if form.is_valid():
            new_crontab = Crontab(
                minute=form.cleaned_data['minute'],
                hour=form.cleaned_data['hour'],
                day=form.cleaned_data['day'],
            )
            new_crontab.save()
            add_cron(new_crontab.minute, new_crontab.hour, new_crontab.day)
            return HttpResponseRedirect(reverse('devices_list_url'))
        else:
            return render(request, 'editordb/add_crontab.html', {'form': form})


class UpdateCrontab(LoginRequiredMixin, View):

    raise_exception = True

    def get(self, request):

        crontab = Crontab.objects.get()
        form = CrontabForm(instance=crontab)
        context = {'form': form, 'crontab': crontab}
        templates = ['editordb/update_crontab.html']
        return render(request, templates, context=context)


    def post(self, request):
        crontab = Crontab.objects.get()
        form = CrontabForm(request.POST, instance=crontab)
        templates = 'editordb/update_crontab.html'

        if form.is_valid():
            update_crontab = form.save()
            add_cron(crontab.minute, crontab.hour, crontab.day)

            return HttpResponseRedirect(reverse('devices_list_url'))
        else:
            return render(request, templates, {'form': form})


class LoginFormView(FormView):

    form_class = AuthenticationForm
    template_name = 'editordb/autheditor.html'
    success_url = 'devices_list/'

    def form_valid(self, form):

        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)
