# Generated by Django 3.0.4 on 2021-07-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0138_createconf_minleftuserfln'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createvisio',
            name='joinurlzoom',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='createvisio',
            name='starturlzoom',
            field=models.TextField(blank=True, null=True),
        ),
    ]
