# Generated by Django 5.1.1 on 2024-11-12 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0022_car_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='user',
            new_name='owner',
        ),
    ]
