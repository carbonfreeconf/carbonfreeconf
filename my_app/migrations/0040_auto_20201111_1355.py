# Generated by Django 3.0.4 on 2020-11-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0039_createconf_fee_to_carbon'),
    ]

    operations = [
        migrations.AddField(
            model_name='createconf',
            name='priv',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private', max_length=9, verbose_name='Public or private conference?'),
        ),
        migrations.AlterField(
            model_name='createconf',
            name='fee_to_carbon',
            field=models.BooleanField(default=False, verbose_name='Should the fees collected be used by us to offset more carbon emissions? (or paid to you?, in this case do not check the box)'),
        ),
    ]
