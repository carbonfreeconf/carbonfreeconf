# Generated by Django 3.0.4 on 2020-11-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0042_auto_20201111_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='twitterhashtag',
            field=models.CharField(default='#CarbonFreeConf', max_length=300, verbose_name='Twitter Hashtag'),
        ),
    ]
