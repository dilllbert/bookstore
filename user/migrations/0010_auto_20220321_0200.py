# Generated by Django 3.1 on 2022-03-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20220321_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='account',
            field=models.CharField(max_length=16, unique=True, verbose_name='帳號'),
        ),
    ]
