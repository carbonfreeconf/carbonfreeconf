# Generated by Django 3.0.4 on 2021-07-23 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0012_remove_question_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='confid',
            field=models.IntegerField(default=0),
        ),
    ]
