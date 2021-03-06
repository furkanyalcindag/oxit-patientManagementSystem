# Generated by Django 3.1.7 on 2021-09-01 15:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0024_auto_20210831_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='clinic',
        ),
        migrations.CreateModel(
            name='PatientClinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
