# Generated by Django 3.0.4 on 2020-11-20 14:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_postview_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postview',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]