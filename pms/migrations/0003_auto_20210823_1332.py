# Generated by Django 3.1.7 on 2021-08-23 10:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0002_auto_20210813_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='assay',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='checkingaccount',
            name='payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='checkingaccount',
            name='protocol',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pms.protocol'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='debtPaidOff',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name='PaymentMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('remainingDebt', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('debtPaidOff', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('checkingAccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pms.checkingaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
