# Generated by Django 5.1.1 on 2024-09-24 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0015_transmissiontype'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='trtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.transmissiontype'),
        ),
    ]
