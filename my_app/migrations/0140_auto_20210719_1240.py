# Generated by Django 3.0.4 on 2021-07-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0139_auto_20210709_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='coffeebreak',
            field=models.BooleanField(default=True, verbose_name='Add a coffee break parallel room that is always accessible?'),
        ),
        migrations.AddField(
            model_name='createconf',
            name='coffeebreakgames',
            field=models.BooleanField(default=True, verbose_name='Add games in the coffee break room?'),
        ),
    ]