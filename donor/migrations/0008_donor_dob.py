# Generated by Django 3.1.6 on 2021-02-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0007_auto_20210215_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='dob',
            field=models.CharField(default='blank', max_length=40),
        ),
    ]
