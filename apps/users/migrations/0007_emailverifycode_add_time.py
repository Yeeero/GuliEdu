# Generated by Django 2.2.6 on 2020-10-15 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201014_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverifycode',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
