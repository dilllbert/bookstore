from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from utils.mixin import LoginRequiredMixin
from django.views.generic import View
from goods.models import Books_sku
from cart.models import *
from user.models import User


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        uid = request.user

        # 查詢此用戶的購物車
        carts=CartInfo.objects.filter(user=uid)
        # 構造上下文

        # 渲染模闆
        return  render(request,'df_cart/cart.html',locals())


class AddtView(LoginRequiredMixin, View):
    def get(self, request):
        #用戶uid購買了gid商品，數量為count
        gid=request.GET.get('gid')
        uid = request.user.id
        cart=CartInfo()
        cart.user=User.objects.get(id=uid)
        cart.goods=Books_sku.objects.get(id=gid)
        cart.count=1
        cart.save()

        tar_good=Books_sku.objects.get(id=gid)
        tar_good.status=0
        tar_good.save()
        
        return HttpResponseRedirect('/goods/?ISBN_Q='+str(tar_good.ISBN.ISBN))

class DeleteView(LoginRequiredMixin, View):
    def get(self, request,cart_id):
        #用戶uid購買了gid商品，數量為count
        try:
            cart=CartInfo.objects.get(id=cart_id)
            cart.delete()
            cart.goods.status=1
            cart.goods.save()
            data={'ok':1}
        except Exception as e:
            data={'ok':0}
        return HttpResponseRedirect('/cart')