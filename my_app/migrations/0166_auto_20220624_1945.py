# Generated by Django 3.0.4 on 2022-06-24 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0165_auto_20220624_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='titleurl',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name="Enter your website's url"),
        ),
    ]
