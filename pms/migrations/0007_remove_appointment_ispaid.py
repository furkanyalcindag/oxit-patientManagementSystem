# Generated by Django 3.1.7 on 2021-08-23 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0006_auto_20210823_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='isPaid',
        ),
    ]