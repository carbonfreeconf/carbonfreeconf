# Generated by Django 3.0.4 on 2021-02-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0093_auto_20210226_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createconf',
            name='fee_currency',
            field=models.CharField(choices=[('Euros', 'Euros'), ('US Dollars', 'US Dollars'), ('GB Pounds', 'GB Pounds')], default='Euros', max_length=15, verbose_name='In which currency?'),
        ),
    ]
