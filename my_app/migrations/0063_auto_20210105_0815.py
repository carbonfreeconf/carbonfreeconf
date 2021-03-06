# Generated by Django 3.0.4 on 2021-01-05 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0062_createquestion_highlight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createconf',
            name='question_last_updated',
        ),
        migrations.CreateModel(
            name='UserUpdateQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_last_updated', models.DateTimeField(null=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.CreateConf')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
