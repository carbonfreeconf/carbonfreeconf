# Generated by Django 3.0.4 on 2021-01-02 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0056_createvisio_celery_task_id_fin'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_score', models.IntegerField(db_index=True, default=0)),
                ('num_vote_up', models.PositiveIntegerField(db_index=True, default=0)),
                ('num_vote_down', models.PositiveIntegerField(db_index=True, default=0)),
                ('question', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('anonymous', models.BooleanField(default=False)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.CreateConf')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
