# Generated by Django 3.1 on 2022-02-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220218_0521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用戶', 'verbose_name_plural': '用戶'},
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='收件地址'),
        ),
    ]
