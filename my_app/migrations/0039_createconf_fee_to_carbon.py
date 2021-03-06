# Generated by Django 3.0.4 on 2020-11-09 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0038_auto_20201022_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='fee_to_carbon',
            field=models.BooleanField(default=False, verbose_name='Should the fees collected be paid to offset more carbon emissions? (or to you? in this case do not check the box)'),
        ),
    ]
