# Generated by Django 3.0.4 on 2020-07-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0018_website_showprogram'),
    ]

    operations = [
        migrations.AddField(
            model_name='createvisio',
            name='vimeo_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
