# Generated by Django 2.1.5 on 2019-02-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editordb', '0014_auto_20190201_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crontab',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='crontab',
            name='day',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='crontab',
            name='hour',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='crontab',
            name='minute',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Days',
        ),
        migrations.DeleteModel(
            name='Hours',
        ),
        migrations.DeleteModel(
            name='Minutes',
        ),
    ]
