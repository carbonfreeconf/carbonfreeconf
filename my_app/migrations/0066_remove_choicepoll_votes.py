# Generated by Django 3.0.4 on 2021-01-12 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0065_userupdateq_poll_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicepoll',
            name='votes',
        ),
    ]