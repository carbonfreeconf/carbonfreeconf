# Generated by Django 3.0.4 on 2021-01-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0060_auto_20210102_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='question_last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
