# Generated by Django 5.1.1 on 2024-09-24 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_car_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enginetype',
            old_name='type',
            new_name='etype',
        ),
    ]
