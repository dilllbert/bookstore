# Generated by Django 3.1 on 2022-02-21 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderinfo_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='order_status',
        ),
        migrations.RemoveField(
            model_name='orderinfo',
            name='trade_no',
        ),
    ]
