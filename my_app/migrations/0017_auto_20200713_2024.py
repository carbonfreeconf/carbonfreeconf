# Generated by Django 3.0.4 on 2020-07-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0016_registerconf_recid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createconf',
            name='privacy',
        ),
        migrations.AddField(
            model_name='createconf',
            name='poster',
            field=models.BooleanField(default=False, verbose_name='Are posters allowed?'),
        ),
        migrations.AlterField(
            model_name='registerconf',
            name='socloc',
            field=models.IntegerField(choices=[(0, 'Not an organizer/decision panel member'), (1, 'Program committee member'), (2, 'Organizer')], default=0),
        ),
    ]
