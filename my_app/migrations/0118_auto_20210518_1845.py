# Generated by Django 3.0.4 on 2021-05-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0117_auto_20210518_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsmaster',
            name='diffemails',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbdiffm',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
