# Generated by Django 3.0.4 on 2021-06-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0122_createconf_activateqandp'),
    ]

    operations = [
        migrations.AddField(
            model_name='createvisio',
            name='mp4_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]