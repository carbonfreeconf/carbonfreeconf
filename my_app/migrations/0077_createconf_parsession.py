# Generated by Django 3.0.4 on 2021-02-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0076_website_color_men'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='parsession',
            field=models.BooleanField(default=True, verbose_name='Participants can access to all parallel sessions?'),
        ),
    ]
