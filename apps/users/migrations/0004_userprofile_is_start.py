# Generated by Django 2.2.6 on 2020-10-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201005_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_start',
            field=models.BooleanField(default=False, verbose_name='是否已激活'),
        ),
    ]