# Generated by Django 2.2.6 on 2020-10-09 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_auto_20201007_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlove',
            old_name='love_name',
            new_name='love_user',
        ),
    ]