# Generated by Django 3.0.4 on 2020-12-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0054_auto_20201219_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerconf',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registerconf',
            name='datetest',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
