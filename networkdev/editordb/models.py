from django.db import models


class ID_production(models.Model):
    production = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.production


class ID_connection_type(models.Model):
    connection_type =  models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.connection_type


class Devices(models.Model):
    ip_address = models.CharField(max_length=15, db_index=True, unique=True)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    location_backups = models.CharField(max_length=100, blank=True)
    production = models.ForeignKey(ID_production, on_delete=models.CASCADE)
    connection_type = models.ForeignKey(ID_connection_type, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip_address

    class Meta:
        ordering = ['id']

class Minutes(models.Model):
    minutes = models.IntegerField()

    def __str__(self):
        return str(self.minutes)


class Hours(models.Model):
    hours = models.IntegerField()

    def __str__(self):
        return str(self.hours)

class Days(models.Model):
    days = models.CharField(max_length=9)

    def __str__(self):
        return self.days

    class Meta:
        ordering = ['id']

class Crontab(models.Model):
    minute = models.ForeignKey(Minutes, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hours, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.day)
