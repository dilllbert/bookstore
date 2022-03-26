from django.contrib import admin
from .models import OrderInfo,OrderDetailinfo

# Register your models here.

admin.site.register(OrderInfo)
admin.site.register(OrderDetailinfo)