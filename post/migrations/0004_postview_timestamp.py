# Generated by Django 3.0.4 on 2020-11-20 14:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='postview',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
