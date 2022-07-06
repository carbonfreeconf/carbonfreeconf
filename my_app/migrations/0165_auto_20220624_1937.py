# Generated by Django 3.0.4 on 2022-06-24 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0164_auto_20220621_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createconf',
            name='titleurl',
        ),
        migrations.AddField(
            model_name='website',
            name='titleurl',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name="Enter your website's url"),
        ),
    ]