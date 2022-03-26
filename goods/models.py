# -*-coding:utf-8-*-
from django.db import models
from db.base_model import BaseModel
from ckeditor.fields import RichTextField
from db.base_model import BaseModel




class Books(BaseModel):


    status_choices = (
        (0, '下線'),
        (1, '上線')
    )
    #商品SPU模型類
    title       = models.TextField(verbose_name='書名')
    ISBN        =models.TextField(verbose_name='ISBN')
    publisher   =  models.TextField(verbose_name='發行商')
    author      =models.TextField(verbose_name='作者名')
    date        = models.TextField(verbose_name='發行日')
    spu_image       = models.TextField(verbose_name='圖片網址')
    # 富文本類型：帶有格式的文本
    detail          =RichTextField(blank=True, verbose_name='商品介紹')
    orginal_price   = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='商品原價')
    type            = models.IntegerField(verbose_name='書的類別')
    all_status=models.SmallIntegerField(default=0, choices=status_choices, verbose_name='總狀態')
    

    class Meta:
        db_table = 'df_books'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class Books_sku(BaseModel):
    """商品sku模型類"""

    status_choices = (
        (0, '下線'),
        (1, '上線')
    )
    User = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='商品持有者' ,default=1)
    ISBN = models.ForeignKey('Books', on_delete=models.CASCADE, verbose_name='商品SPU')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='預售價格')
    file = models.FileField(upload_to='videos/', null=True, verbose_name="商品影片")
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='狀態')


    class Meta:
        db_table = 'df_books_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name