# Generated by Django 3.0.4 on 2021-02-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0096_auto_20210226_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createconf',
            name='fee_amount',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Fee they must pay'),
        ),
    ]
