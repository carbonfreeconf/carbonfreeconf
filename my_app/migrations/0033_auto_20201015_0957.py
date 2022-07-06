# Generated by Django 3.0.4 on 2020-10-15 09:57

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0032_website_color_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='color_text',
            field=colorfield.fields.ColorField(default='#fff', max_length=18, verbose_name='Text color on the conference website'),
        ),
        migrations.AlterField(
            model_name='website',
            name='color_background',
            field=colorfield.fields.ColorField(default='#223', max_length=18, verbose_name='Background color on the conference website'),
        ),
    ]