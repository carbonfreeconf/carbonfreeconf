# Generated by Django 3.0.4 on 2021-06-10 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0124_createconf_finishimport'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsmaster',
            name='bestposter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.RegisterConf'),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='votes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
