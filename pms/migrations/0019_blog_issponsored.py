# Generated by Django 3.1.7 on 2021-08-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0018_doctoreducation_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='isSponsored',
            field=models.BooleanField(default=False),
        ),
    ]