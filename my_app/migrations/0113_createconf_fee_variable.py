# Generated by Django 3.0.4 on 2021-05-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0112_auto_20210505_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='fee_variable',
            field=models.BooleanField(default=False, verbose_name='Participants can give what they want'),
        ),
    ]
