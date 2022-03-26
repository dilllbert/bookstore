from django.urls import path,include, re_path
from order.views import OrderConView,OrderCommitView
app_name = 'order'
urlpatterns = [
        re_path(r'^$',OrderConView.as_view()),
        path('commit',OrderCommitView.as_view()),
]
