# Generated by Django 3.0.4 on 2021-02-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0079_auto_20210210_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='createpoll',
            name='change',
            field=models.BooleanField(default=False),
        ),
    ]