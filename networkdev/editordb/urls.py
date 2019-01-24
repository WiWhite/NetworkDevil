from django.urls import path
from .views import *

urlpatterns = [
    path('', DevicesView.as_view(), name='devices_list_url'),
    path('add_device/', AddDevice.as_view(), name='add_device_url'),
    path('<int:id>/update_device/', UpdateDevice.as_view(), name='update_device_url'),
    path('<int:id>/delete_device/', DeleteDevice.as_view(), name='delete_device_url'),
    path('add_crontab/', AddCrontab.as_view(), name='add_crontab_url'),
    path('update_crontab/', UpdateCrontab.as_view(), name='update_crontab_url'),
]