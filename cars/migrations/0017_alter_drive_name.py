# Generated by Django 5.1.1 on 2024-11-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_car_trtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drive',
            name='name',
            field=models.TextField(verbose_name='Тип привода'),
        ),
    ]