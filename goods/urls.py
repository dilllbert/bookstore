from django.conf import settings
from django.urls import path,include, re_path
from goods.views import  index, ListView,DetailView
from . import views
from django.conf.urls.static import static
app_name = 'goods'
urlpatterns = [
     re_path(r'^index/$',index, name='index'),
     path('list/<int:typeid>', ListView.as_view(), name='list'), 
     path('goods/', DetailView.as_view(), name='detail'),     
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)