# Generated by Django 5.1.1 on 2024-11-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0018_drive_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodytype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='enginetype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='transmissiontype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]