from django.urls import path,include, re_path
from cart.views import CartView,AddtView,DeleteView
import cart.views
app_name = 'cart'
urlpatterns = [
     # 購物車展示
    re_path(r'^$',CartView.as_view(),name='cart'),
    path('add/',AddtView.as_view()),
    re_path(r'^delete(\d+)/$',DeleteView.as_view()),
    # 購物車商品增加
]
