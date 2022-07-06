# Generated by Django 3.0.4 on 2021-05-18 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0116_statsmaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsmaster',
            name='CO2m',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='countvdurationm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='countvm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='countvviewm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='finished',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbattonlym',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbhourzoomm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbmesm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbmespom',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbpartm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbpartsevensubmm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbpartsm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbparttotm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbpostersm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbpostsm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbroomm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbtalksm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='nbviewpm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statsmaster',
            name='timeoverm',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
