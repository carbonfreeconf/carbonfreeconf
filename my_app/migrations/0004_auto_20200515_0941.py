# Generated by Django 3.0.4 on 2020-05-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_transac_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='transac',
            name='amountafterdiscountprep',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='transac',
            name='amountoff',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='transac',
            name='amountprep',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='transac',
            name='coupon',
            field=models.CharField(max_length=15, null=True),
        ),
    ]