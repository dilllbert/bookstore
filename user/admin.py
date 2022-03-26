from django.contrib import admin

# Register your models here.
from user.models import User,Address, Card
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Card)