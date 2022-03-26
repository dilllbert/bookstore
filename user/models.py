from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """用戶模型類"""
    class Meta:
        db_table = 'df_user'
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

class Address(BaseModel):
    """地址模型類"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所屬用戶')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    phone = models.CharField(max_length=11, verbose_name='聯係電話')
    is_default = models.BooleanField(default=False, verbose_name='是否默認')

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name


class Card(BaseModel):
    """地址模型類"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所屬用戶')
    account = models.CharField(max_length=16, verbose_name='帳號',unique=True)
    holder = models.CharField(max_length=20, verbose_name='持卡人姓名')
    dueday = models.CharField(max_length=4, verbose_name='到期日')
    cvv=models.CharField(max_length=3,verbose_name='cvv')
    is_default = models.BooleanField(default=False, verbose_name='是否默認')

    class Meta:
        db_table = 'df_card'
        verbose_name = '銀行帳戶'
        verbose_name_plural = verbose_name
