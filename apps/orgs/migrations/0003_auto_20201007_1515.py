# Generated by Django 2.2.6 on 2020-10-07 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_auto_20201005_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orginfo',
            old_name='cifyinfo',
            new_name='cityyinfo',
        ),
    ]
