# Generated by Django 3.1.7 on 2021-08-29 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0017_clinicmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoreducation',
            name='doctor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pms.staff'),
            preserve_default=False,
        ),
    ]
