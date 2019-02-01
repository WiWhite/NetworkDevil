from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name='autheditor_url'),
    path('devices_list/', DevicesView.as_view(), name='devices_list_url'),
    path('add_device/', AddDevice.as_view(), name='add_device_url'),
    path(
        'devices_list/<int:id>/update_device/',
        UpdateDevice.as_view(),
        name='update_device_url'
        ),
    path(
        'devices_list/<int:id>/delete_device/',
        DeleteDevice.as_view(),
        name='delete_device_url'
        ),
    path('add_crontab/', AddCrontab.as_view(), name='add_crontab_url'),
    path('update_crontab/', UpdateCrontab.as_view(), name='update_crontab_url'),
    path(
        'devices_list/<int:id>/diff_backups',
        DiffDevice.as_view(),
        name='diff_backups_url'
        ),
]
