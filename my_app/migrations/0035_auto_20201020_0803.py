# Generated by Django 3.0.4 on 2020-10-20 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0034_auto_20201019_1533'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-updated_on']},
        ),
        migrations.AddField(
            model_name='website',
            name='share',
            field=models.BooleanField(default=False, verbose_name='Show the twitter and facebook share buttons at the bottom of the conference website?'),
        ),
    ]
