# Generated by Django 3.0.4 on 2021-02-13 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0087_userprofileinfo_lastlogintimepanel'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerconf',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='registerconf',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
