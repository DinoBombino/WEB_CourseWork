# Generated by Django 5.1.1 on 2024-11-24 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0026_rename_owner_car_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='user',
        ),
    ]
