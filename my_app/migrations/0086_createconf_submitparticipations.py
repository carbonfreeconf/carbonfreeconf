# Generated by Django 3.0.4 on 2021-02-12 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0085_auto_20210211_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='submitparticipations',
            field=models.BooleanField(default=True, verbose_name='Can the participants submit participations?'),
        ),
    ]