# Generated by Django 3.1.2 on 2020-10-05 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherinfo',
            name='gender',
            field=models.CharField(choices=[('boy', '男'), ('girl', '女')], default='boy', max_length=10),
        ),
    ]
