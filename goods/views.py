#coding=utf-8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from goods.models import Books_sku,Books
from django.core.paginator import Paginator
from django.views.generic import View
import json
# Create your views here.
def index(request):
    return render(request,'df_goods/index.html')

class ListView(View):
    def get(self, request,typeid):
        page_num = request.GET.get('page',1)
        type_result = Books.objects.filter(type=typeid).order_by("ISBN")
        paginator = Paginator(type_result,4)
        print(page_num)
        try:
            c_page = paginator.page(int(page_num))
        except Exception as e:
            page = 1
        return render(request, 'df_goods/list.html',locals())


class DetailView(View):
    """詳情頁"""
    def get(self, request):
        try:
            ISBN_R=request.GET.get('ISBN_Q',1)
            print(ISBN_R)
            try:
                book = Books.objects.get(ISBN=ISBN_R)
                Books_sku_res=Books_sku.objects.filter(ISBN=book)
                for booksku in Books_sku_res:
                    if booksku.status == 1:
                        book.status = 1
                        break
                return render(request, 'df_goods/detail.html',locals())

            except:
                ISBN=ISBN_R

                book = Books.objects.filter(title__contains= ISBN_R).order_by("ISBN")
               
                if not book.exists():
                    return render(request, 'df_goods/nb.html')
                page_num = request.GET.get('page',1)

                paginator = Paginator(book,4)
                try:
                    c_page = paginator.page(int(page_num))
                except Exception as e:
                    page = 1
                return render(request, 'df_goods/listbysearch.html',locals())

        except Books.DoesNotExist:
            return render(request, 'df_goods/nb.html')



        





