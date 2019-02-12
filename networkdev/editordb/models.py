from django.db import models
from django.core.validators import validate_ipv4_address
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class ID_production(models.Model):
    production = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.production


class ID_connection_type(models.Model):
    connection_type =  models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.connection_type


class Devices(models.Model):
    ip_address = models.CharField(
                            max_length=15,
                            db_index=True,
                            unique=True,
                            validators=[validate_ipv4_address]
                            )
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    location_backups = models.CharField(max_length=100, blank=True)
    production = models.ForeignKey(ID_production, on_delete=models.CASCADE)
    connection_type = models.ForeignKey(
                                 ID_connection_type,
                                 on_delete=models.CASCADE
                                 )

    def __str__(self):
        return self.ip_address

    class Meta:
        ordering = ['id']

def validate_day(value):
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'ED']
    if value not in days:
        raise ValidationError('{} is not in {}'.format(value, days))


class Crontab(models.Model):
    minute = models.IntegerField(
                      validators=[MinValueValidator(0), MaxValueValidator(59)]
                      )
    hour = models.IntegerField(
                      validators=[MinValueValidator(0), MaxValueValidator(23)]
                      )
    day = models.CharField(
                      max_length=3, unique=True, validators=[validate_day]
                      )

    def __str__(self):
        return str(self.day)


    class Meta:
        ordering = ['id']
