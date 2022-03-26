#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author:lisen
@file:base_model.py
@time:2019/02/27
"""
from django.db import models


class BaseModel(models.Model):
    """模型抽象基類"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    is_delete = models.BooleanField(default=False, verbose_name='刪除標記')

    class Meta:
        abstract = True  # 說明是一個抽象模型類
