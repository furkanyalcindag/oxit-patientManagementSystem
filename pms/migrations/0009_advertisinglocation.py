# Generated by Django 3.1.7 on 2021-07-29 11:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0008_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('width', models.CharField(max_length=256)),
                ('height', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
