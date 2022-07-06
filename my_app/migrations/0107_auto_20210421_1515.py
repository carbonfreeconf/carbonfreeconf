# Generated by Django 3.0.4 on 2021-04-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0106_auto_20210415_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='onlypabstract',
            field=models.BooleanField(default=False, verbose_name='Abstracts showed only to validated participants?'),
        ),
        migrations.AddField(
            model_name='website',
            name='onlypposter',
            field=models.BooleanField(default=False, verbose_name='Posters showed only to validated participants?'),
        ),
        migrations.AddField(
            model_name='website',
            name='onlypprogram',
            field=models.BooleanField(default=False, verbose_name='Program showed only to validated participants?'),
        ),
        migrations.AlterField(
            model_name='programdesign',
            name='opacity',
            field=models.IntegerField(default=10, verbose_name='Opacity of the boxes'),
        ),
    ]