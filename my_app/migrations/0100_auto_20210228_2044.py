# Generated by Django 3.0.4 on 2021-02-28 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0099_auto_20210228_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createquestion',
            name='question',
            field=models.TextField(null=True),
        ),
    ]