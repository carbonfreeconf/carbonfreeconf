# Generated by Django 3.0.4 on 2020-10-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0029_auto_20201009_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='messagetoall',
            field=models.TextField(default='message', max_length=500, verbose_name='Message to all participants'),
            preserve_default=False,
        ),
    ]