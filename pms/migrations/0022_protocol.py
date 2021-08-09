# Generated by Django 3.1.7 on 2021-08-04 08:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0021_assay'),
    ]

    operations = [
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=1028)),
                ('barcode', models.CharField(max_length=256)),
                ('assay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.assay')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]