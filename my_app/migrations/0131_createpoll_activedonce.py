# Generated by Django 3.0.4 on 2021-07-06 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0130_userprofileinfo_instcountry'),
    ]

    operations = [
        migrations.AddField(
            model_name='createpoll',
            name='activedonce',
            field=models.BooleanField(default=False),
        ),
    ]