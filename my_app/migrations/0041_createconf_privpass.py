# Generated by Django 3.0.4 on 2020-11-11 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0040_auto_20201111_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='privpass',
            field=models.CharField(default='', max_length=20),
        ),
    ]
