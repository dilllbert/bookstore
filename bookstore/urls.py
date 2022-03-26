"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls'), name='user'),  # 用户模块
    path('cart/', include('cart.urls'), name='cart'),  # 购物车模块
    path('order/', include('order.urls'), name='order'),  # 订单模块
    path('', include('goods.urls'), name='goods'),  # 商品模块
    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)