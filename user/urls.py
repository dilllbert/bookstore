from django.urls import path,include, re_path
from user.views import AddressView, BankDeleteadView, Bankset, DeleteView, DeleteadView, GinView, PayRView, PayView, PostHandleView,  RegisterView, ActiveView,LoginView,LogoutView,OrderDetailView,PostView,UserInfoView, UserOrderView, useragree
from . import views
app_name = 'user'

urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name='register'),  
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),  
    re_path(r'^$', UserInfoView.as_view(), name='user'),  
    re_path(r'^address/$', AddressView.as_view(), name='address'), 
    re_path(r'^posthandle', PostHandleView.as_view(), name='posthandle'),  
    re_path(r'^postdelete(\d+)/$', DeleteView.as_view(), name='delete'),  
    re_path(r'^pay/', PayView.as_view(), name='delete'), 
    re_path(r'^post', PostView.as_view(), name='seller'),  
    path("orderdetail/",OrderDetailView.as_view()),
    re_path(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),
    path("user_agreement/",useragree.as_view()),
    re_path(r'^delete(\d+)/$',DeleteadView.as_view()),
    re_path(r'^bankdelete(\d+)/$',BankDeleteadView.as_view(), name='bankdel'),
    re_path(r'^setbank(\d+)/$',Bankset.as_view(), name='bankset'),
    re_path(r'^bank/$',PayRView.as_view(), name='bank'),
    re_path(r'^gin/$',GinView.as_view()),

]