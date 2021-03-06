# Generated by Django 3.0.4 on 2020-07-20 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0021_createvisio_celery_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerconf',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='registerconf',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='registerconf',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
