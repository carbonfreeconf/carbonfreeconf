# Generated by Django 3.0.4 on 2021-08-27 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0155_auto_20210827_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createconf',
            name='fee_currency',
            field=models.CharField(choices=[('Euros', 'Euros'), ('US Dollars', 'US Dollars'), ('GB Pounds', 'GB Pounds')], default='Euros', max_length=15, verbose_name='In which currency?'),
        ),
        migrations.AlterField(
            model_name='createconf',
            name='fee_currency_unique',
            field=models.CharField(choices=[('Euros', 'Euros'), ('US Dollars', 'US Dollars'), ('GB Pounds', 'GB Pounds')], default='Euros', max_length=15, verbose_name='Choose the currency of most participants that will be proposed by default'),
        ),
    ]
