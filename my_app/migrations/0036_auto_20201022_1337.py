# Generated by Django 3.0.4 on 2020-10-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0035_auto_20201020_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerconf',
            name='testvirtualroom',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='registerconf',
            name='abstract',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Abstract'),
        ),
        migrations.AlterField(
            model_name='registerconf',
            name='title',
            field=models.CharField(blank=True, max_length=300, verbose_name='Title'),
        ),
    ]
