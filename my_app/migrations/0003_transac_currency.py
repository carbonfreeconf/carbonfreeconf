# Generated by Django 3.0.4 on 2020-05-15 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_auto_20200514_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='transac',
            name='currency',
            field=models.CharField(default='EUR', max_length=10),
        ),
    ]