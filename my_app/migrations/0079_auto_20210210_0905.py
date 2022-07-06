# Generated by Django 3.0.4 on 2021-02-10 09:05

import conf.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0078_createquestion_pollimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createquestion',
            name='pollimage',
        ),
        migrations.AddField(
            model_name='createpoll',
            name='pollimage',
            field=models.ImageField(blank=True, null=True, storage=conf.storage_backends.PublicMediaStorage(), upload_to='static/pollimages/', verbose_name=''),
        ),
    ]