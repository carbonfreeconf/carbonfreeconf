# Generated by Django 3.0.4 on 2021-08-25 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0147_auto_20210824_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='showdoc',
            field=models.BooleanField(default=False, verbose_name='Show a page with conference documents (slides/posters/papers)?'),
        ),
    ]