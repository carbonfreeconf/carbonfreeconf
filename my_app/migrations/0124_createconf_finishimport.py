# Generated by Django 3.0.4 on 2021-06-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0123_createvisio_mp4_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='finishimport',
            field=models.BooleanField(default=False),
        ),
    ]
