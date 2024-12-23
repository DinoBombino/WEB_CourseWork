# Generated by Django 5.1.1 on 2024-09-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0012_delete_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btype', models.TextField(verbose_name='Тип кузова')),
            ],
            options={
                'verbose_name': 'Тип кузова',
                'verbose_name_plural': 'Типы кузовов',
            },
        ),
        migrations.AlterField(
            model_name='enginetype',
            name='etype',
            field=models.TextField(verbose_name='Тип двигателя'),
        ),
    ]
