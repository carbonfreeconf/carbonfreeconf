# Generated by Django 3.0.4 on 2021-02-05 10:29

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0071_auto_20210205_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='color_menu',
            field=colorfield.fields.ColorField(default='#ffffff88', max_length=18, verbose_name='Menu color on the conference website'),
        ),
    ]
