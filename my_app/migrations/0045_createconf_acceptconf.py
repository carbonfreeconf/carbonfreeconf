# Generated by Django 3.0.4 on 2020-11-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0044_auto_20201117_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='acceptconf',
            field=models.BooleanField(default=False),
        ),
    ]
