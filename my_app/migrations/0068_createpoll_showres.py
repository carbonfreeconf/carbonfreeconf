# Generated by Django 3.0.4 on 2021-01-12 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0067_createpoll_removed'),
    ]

    operations = [
        migrations.AddField(
            model_name='createpoll',
            name='showres',
            field=models.BooleanField(default=False),
        ),
    ]
