# Generated by Django 3.0.4 on 2020-05-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_auto_20200518_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='isinconf',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='proceeding',
            name='bibtex',
            field=models.TextField(blank=True, null=True, verbose_name=''),
        ),
    ]
