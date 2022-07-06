# Generated by Django 3.0.4 on 2021-02-05 12:37

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0075_remove_website_color_men'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='color_men',
            field=colorfield.fields.ColorField(default='#888888', max_length=18, verbose_name='Menu color on the conference website'),
        ),
    ]
