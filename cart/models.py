#coding=utf-8

from django.db import models
# 購物車模型
class CartInfo(models.Model):
    # 外鍵用戶
    user=models.ForeignKey('user.User',on_delete=models.CASCADE)
    # 外鍵商品
    goods=models.ForeignKey('goods.Books_sku',on_delete=models.CASCADE,)
    # 購買的數量
    count=models.IntegerField()