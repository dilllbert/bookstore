# Generated by Django 3.1 on 2022-03-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220222_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='創建時間'),
        ),
        migrations.AlterField(
            model_name='address',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='刪除標記'),
        ),
        migrations.AlterField(
            model_name='address',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新時間'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='創建時間'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='刪除標記'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新時間'),
        ),
    ]