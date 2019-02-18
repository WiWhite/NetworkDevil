# Generated by Django 2.1.5 on 2019-02-18 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editordb', '0016_auto_20190215_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='crontab',
            name='ttl_backups',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)]),
        ),
    ]