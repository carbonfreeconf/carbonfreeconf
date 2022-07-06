# Generated by Django 3.0.4 on 2021-05-16 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0114_chatcanal'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosterView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('number', models.CharField(blank=True, max_length=100)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.RegisterConf')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
