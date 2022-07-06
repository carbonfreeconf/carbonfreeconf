# Generated by Django 3.0.4 on 2021-08-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0148_website_showdoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerconf',
            name='paperurl',
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='registerconf',
            name='slideshow',
            field=models.BooleanField(default=False),
        ),
    ]
