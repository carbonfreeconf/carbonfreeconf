# Generated by Django 3.0.4 on 2021-05-15 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0113_createconf_fee_variable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatCanal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titleg', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('topic', models.CharField(max_length=300, null=True)),
                ('people', models.TextField(null=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.CreateConf')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]