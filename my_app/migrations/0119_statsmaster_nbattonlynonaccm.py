# Generated by Django 3.0.4 on 2021-05-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0118_auto_20210518_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsmaster',
            name='nbattonlynonaccm',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
