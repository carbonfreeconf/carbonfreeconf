# Generated by Django 3.0.4 on 2022-06-30 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0172_heropicture_heroname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='slug',
        ),
    ]
