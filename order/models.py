from django.db import models
from db.base_model import BaseModel
from goods.models import Books_sku
from user.models import User,Card

class OrderInfo(BaseModel):
    """訂單模型類"""

    PAY_METHOD_CHOICES = (
        (1, '貨到付款'),
        (2, '銀行轉帳'),
        (3, '信用卡/金融卡'),
    )

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用戶')
    addr = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name='地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='支付方式')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='總金額')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='運費')
    date = models.DateTimeField(verbose_name='購買日期',auto_now=True)
    card = models.ForeignKey('user.Card', on_delete=models.CASCADE, verbose_name='銀行卡號',null=True)


    class Meta:
        db_table = 'df_order_info'
        verbose_name = '訂單'
        verbose_name_plural = verbose_name

class OrderDetailinfo(BaseModel):
    """訂單商品模型類"""
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='訂單')
    sku = models.ForeignKey('goods.Books_sku', on_delete=models.CASCADE, verbose_name='商品SKU')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '訂單商品'
        verbose_name_plural = verbose_name


