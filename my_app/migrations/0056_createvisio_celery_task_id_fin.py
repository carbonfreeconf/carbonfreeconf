# Generated by Django 3.0.4 on 2020-12-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0055_auto_20201222_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='createvisio',
            name='celery_task_id_fin',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
