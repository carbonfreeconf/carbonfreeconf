# Generated by Django 3.0.4 on 2021-02-28 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0098_auto_20210227_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createquestion',
            name='question',
            field=models.TextField(null=True, verbose_name='Ask a question to the speaker here'),
        ),
    ]
