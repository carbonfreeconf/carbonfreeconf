# Generated by Django 3.0.4 on 2020-05-15 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_auto_20200515_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transac',
            old_name='amountafterdiscountprep',
            new_name='discount',
        ),
        migrations.AddField(
            model_name='transac',
            name='discountispercentage',
            field=models.BooleanField(null=True),
        ),
    ]