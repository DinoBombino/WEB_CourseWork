# Generated by Django 5.1.1 on 2024-11-12 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0024_rename_owner_car_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='user',
            new_name='owner',
        ),
    ]
