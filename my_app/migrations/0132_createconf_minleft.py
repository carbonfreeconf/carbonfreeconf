# Generated by Django 3.0.4 on 2021-07-08 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0131_createpoll_activedonce'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='minleft',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
