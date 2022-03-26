from django.contrib import admin
from .models import Books,Books_sku

# Register your models here.

admin.site.register(Books)
admin.site.register(Books_sku)