# Generated by Django 5.1.1 on 2024-09-17 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_rename_cars_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterField(
            model_name='car',
            name='drive',
            field=models.TextField(verbose_name='Привод'),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.TextField(verbose_name='Название'),
        ),
    ]
