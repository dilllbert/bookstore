# Generated by Django 3.1 on 2022-03-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='account',
            field=models.CharField(max_length=16, verbose_name='帳號'),
        ),
    ]