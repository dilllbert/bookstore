#coding=utf-8

from xml.etree.ElementTree import QName
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from user.models import Address, Card, User
from cart.models import CartInfo
from goods.models import Books_sku
from django.db import transaction
from order.models import OrderDetailinfo,OrderInfo
from datetime import datetime
from decimal import Decimal
import re



# /order/confirm
class OrderConView(LoginRequiredMixin, View):
    """提交訂單頁麵"""
    def post(self, request):
        # 獲取參數，一鍵多值 接受到的是列錶
        cart_ids = request.POST.getlist('cart_id')
        # 進行參數校驗
        if not all(cart_ids) or len(cart_ids) < 1:
            # 冇有商品id，重定嚮到購物車頁麵進行選擇
            return HttpResponseRedirect(reverse('cart:cart'))

        user = request.user
        addrs = Address.objects.filter(user=user)
        try:
            card = Card.objects.filter(user=user)
        except:
            card = None
        skus = []
        # 初始化總的數量和總價
        total_count = 0
        total_price = 0
        # 查詢對應的商品信息
        for cart_id in cart_ids:
            sku = Books_sku.objects.get(id=cart_id)

            amount = sku.price 
            # 動態的給sku對象添加數量和小計
            sku.amount = amount
            # 計算總的數量和總價
            total_count += 1
            total_price += amount
            skus.append(sku)

        # 運費：運費子係統
        transit_price = 10
        transit_total = transit_price*total_count
        # 實付款
        total_pay = total_price + transit_price*total_count

        return render(request, 'df_order/order.html', locals())


class OrderCommitView(View):
    """訂單創建"""
    def post(self, request):
        
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用戶未登錄'})

        # 接收參數
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
            
       

        
        try:
            sku_ids = request.POST.get('sku_ids')
        except:
            pass
        # 校驗參數
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '參數不完整'})

        try:
            addr = Address.objects.get(id=addr_id)
            print(addr.addr)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '非法地址'})

        # 訂單總金額和總數量
        total_count = 0
        total_price = 0
        # 運費

        sku_ids = sku_ids.split(',')


        for cart_id in sku_ids :
            x=cart_id.find("(")
            y=cart_id.find(")")
            sku = Books_sku.objects.select_for_update().get(id=int(cart_id[x+1:y]))

            amount = sku.price 
            # 動態的給sku對象添加數量和小計
            sku.amount = amount
            # 計算總的數量和總價
            total_count += 1
            total_price += amount

        # 運費：運費子係統
        transit_price = 10
        transit_total = transit_price*total_count
        # 實付款
        total_pay = total_price + transit_price*total_count
        try:
            card = request.POST.get('card')
            card = Card.objects.get(id=card)
            
        except:
            if( pay_method == "3"):    
                return JsonResponse({'errmsg': '未輸入金融帳戶'})
        # todo: 保存訂單信息錶: 嚮df_orderno_info錶中添加一條記錄
        order = OrderInfo.objects.create(
            user=user,
            addr=addr,
            pay_method=pay_method,
            total_price=total_price,
            transit_price=transit_total,
            card=card,
        )
        
        
        for sku_id in sku_ids:
            x=sku_id.find("(")
            y=sku_id.find(")")
            sku = Books_sku.objects.select_for_update().get(id=int(sku_id[x+1:y]))
            
            cart=CartInfo.objects.filter(goods=sku).filter(user=user)
            # todo: 嚮訂單商品錶中添加信息
            OrderDetailinfo.objects.create(
                order=order,
                sku=sku,
            )
            cart.delete()

        return JsonResponse({'res': 5, 'message': '訂單創建成功'})