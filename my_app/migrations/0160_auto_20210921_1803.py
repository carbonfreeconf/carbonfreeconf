# Generated by Django 3.0.4 on 2021-09-21 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0159_auto_20210921_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createconf',
            name='justtools',
            field=models.BooleanField(default=False, verbose_name='We will just use the CarbonFreeConf tools (e.g. abstract management, website creation, participant and program handling, ...) for free but not run the actual conference with the CarbonFreeConf videoconfering tools'),
        ),
    ]
