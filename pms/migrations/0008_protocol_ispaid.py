# Generated by Django 3.1.7 on 2021-08-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0007_remove_appointment_ispaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocol',
            name='isPaid',
            field=models.BooleanField(default=False),
        ),
    ]