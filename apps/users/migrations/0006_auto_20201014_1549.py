# Generated by Django 2.2.6 on 2020-10-14 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201006_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('female', '女'), ('male', '男')], max_length=10, verbose_name='用户性别'),
        ),
    ]