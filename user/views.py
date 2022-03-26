from datetime import timedelta, timezone
import datetime
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
import re
from cart.models import CartInfo
from order.models import OrderDetailinfo, OrderInfo
from utils.mixin import LoginRequiredMixin
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from goods.models import Books_sku,Books
from user.models import User,Address, Card
from goods.models import Books_sku
# Create your views here.
        
class RegisterView(View):
    """註冊"""
    def get(self, request):
        # 顯示註冊頁麵
        return render(request, 'df_user/register.html')

    def post(self, request):
        # 進行註冊處理
        # 接收數據
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 進行數據校驗
        if not all([username, password, email]):
            # 數據不完整
            return render(request, 'df_user/register.html', {'errmsg': '數據不完整'})

        # 檢驗郵箱
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return render(request, 'df_user/register.html', {'errmsg': '郵箱格式不正確'})

        if allow != 'on':
            return render(request, 'df_user/register.html', {'errmsg': '請同意協議'})

        # 校驗用戶是否重複
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用戶名不存在
            user = None

        if user:
            return render(request, 'df_user/register.html', {'errmsg': '用戶已存在'})

        # 進行業務處理：進行用戶註冊
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 發送激活鏈接，包含激活鏈接：http://127.0.0.1:8000/user/active/5
        # 激活鏈接中需要包含用戶的身份信息，並要把身份信息進行加密
        # 激活鏈接格式: /user/active/用戶身份加密後的信息 /user/active/token

        # 加密用戶的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode('utf8')  # 解碼, str

        # 發郵箱
        subject = '請完成郵箱認證'
        message = ''
        sender = settings.EMAIL_PROM  # 發送人
        receiver = [email]
        html_message = '<h1>請點擊以下URL完成認證操作。</h1>' \
                    '<a href="http://127.0.0.1:8000/user/active/%s">' \
                    'http://127.0.0.1:8000/user/active/%s' \
                    '</a>' % (token, token)
    
        send_mail(subject, message, sender, receiver, html_message=html_message)


        # 返回應答,跳轉首頁
        return HttpResponseRedirect(reverse('goods:index'))


# /user/active/加密信息token
class ActiveView(View):
    """用戶激活"""
    def get(self, request, token):
        # 進行用戶激活
        # 進行解密，獲取要激活的用戶信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 獲取待激活用戶的id
            user_id = info['confirm']

            # 根據id獲取用戶信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳轉到登錄頁麵
            return HttpResponseRedirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活鏈接已過期
            return HttpResponse('激活鏈接已失效')

# /user/login
class LoginView(View):
    """登錄"""
    def get(self, request):
        # 顯示登錄頁麵
        # 判斷是否記住密碼
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')  # request.COOKIES['username']
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'df_user/login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # 接受數據
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # remember = request.POST.get('remember')  # on

        # 校驗數據
        if not all([username, password]):
            return render(request, 'df_user/login.html', {'errmsg': '數據不完整、或是用戶信箱未經過驗證'})

        # 業務處理: 登陸校驗
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # print("User is valid, active and authenticated")
                login(request, user)  # 登錄並記錄用戶的登錄狀態

                # 獲取登錄後所要跳轉到的地址, 默認跳轉首頁
                next_url = request.GET.get('next', reverse('goods:index'))

                #  跳轉到next_url
                response = HttpResponseRedirect(next_url)  # HttpResponseRedirect

                # 設置cookie, 需要通過HttpReponse類的實例對象, set_cookie
                # HttpResponseRedirect JsonResponse

                # 判斷是否需要記住用戶名
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                    response.set_cookie('user_id', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # 回應 response
                return response

            else:
                # print("The passwoed is valid, but the account has been disabled!")
                return render(request, 'df_user/login.html', {'errmsg': '賬戶未激活'})
        else:
            return render(request, 'df_user/login.html', {'errmsg': '用戶名、密碼錯誤、或申請信箱未經過驗證'})

class LogoutView(View):
    """退出登錄"""
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    """用戶中心-信息頁"""
    def get(self, request):
        # 獲取個人信息
        user = request.user
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address = None  # 不存在默認地址

        return render(request, 'df_user/user_center_info.html', locals())


class AddressView(LoginRequiredMixin, View):
    """用戶中心-地址頁"""
    def get(self, request):
        user = request.user

        try:
            address =  Address.objects.filter(user=user)
        except Address.DoesNotExist:
            address = None  # 不存在默認地址

        return render(request, 'df_user/user_center_site.html', {'title': '用戶中心-收貨地址', 'page': 'address', 'address': address})

    def post(self, request):
        # 地址添加
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 業務處理：地址添加
        # 如果用戶冇存在默認地址，則添加的地址作為默認收獲地址
        user = request.user

        try:
             address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
             address = None  # 不存在默認地址

        if address:
            is_default = False
        else:
            is_default = True

        # 數據校驗
        if not all([receiver, addr, phone]):
            return render(request, 'df_user/user_center_site.html',
                          {'page': 'address',
                           'address': address,
                           'errmsg': '數據不完整'})

        # 添加
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               phone=phone,
                               is_default=is_default)

        # 返回應答
        try:
            request.POST.get('addr_id')
            return HttpResponseRedirect(reverse('user:address'))
        except:
            return HttpResponseRedirect(reverse('cart:cart'))  # get的請求方式

class PostView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        books=Books_sku.objects.filter(User=user).order_by("status")
        return render(request, 'df_user/post.html', locals())

class PostHandleView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        post_ISBN = request.POST.get('ISBN')
        post_price = request.POST.get('price')
        post_goods_video = request.FILES['goods_video']
        if not all([post_ISBN, post_price, post_goods_video]):
            return render(request, 'df_user/post.html', {'errmsg': '輸入不完整'})
        else:
            Book = Books.objects.get(ISBN=post_ISBN)
            sku  = Books_sku.objects.create(
                ISBN  = Book,
                price = post_price,
                file  = post_goods_video,
                User  = user
            )
        return HttpResponseRedirect('/user/post')


class DeleteView(LoginRequiredMixin, View):
    def get(self, request,cart_id):
        print(cart_id)
        bok=Books_sku.objects.get(id=cart_id)
        bok.delete()
        return HttpResponseRedirect('/user/post')


class UserOrderView(LoginRequiredMixin, View):
    """用戶中心-訂單頁"""
    def get(self, request, page):
        # 獲取用戶的訂單信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('date')

        # 遍曆獲取訂單商品信息
        for order in orders:
            # 根據order_id查詢訂單商品信息
            order_skus = OrderDetailinfo.objects.filter(order = order)


        # 分頁
        paginator = Paginator (orders, 10)  # 單頁顯示數目2

        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages or page <= 0:
            page = 1

        # 獲取第page頁的Page實例對象
        order_page = paginator.page(page)

        # todo: 進行頁碼的控製，頁麵上最多顯示5個頁碼
        # 1. 總數不足5頁，顯示全部
        # 2. 如當前頁是前3頁，顯示1-5頁
        # 3. 如當前頁是後3頁，顯示後5頁
        # 4. 其他情況，顯示當前頁的前2頁，當前頁，當前頁的後2頁
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages-4, num_pages+1)
        else:
            pages = range(page-2, page+3)


        return render(request, 'df_user/user_center_order.html', locals())


class OrderDetailView(LoginRequiredMixin, View):

    def get(self, request):
        orderid=request.GET.get("order_id")
        order = OrderInfo.objects.select_for_update().get(id=int(orderid))
        print(order)
        skuinfos=OrderDetailinfo.objects.filter(order=order)
        return render(request, 'df_user/order_detail.html', locals())

class useragree(View):
    def get(self, request):
        return render(request, 'df_user/user_agreement.html')


class PayView(LoginRequiredMixin, View):
    def get(self, request):
        order_id=request.GET.get("order_id")
        ord= OrderInfo.objects.get(id=order_id)
        x = datetime.datetime.now(timezone.utc)
        pay_due=ord.date+timedelta(hours=48)
        delta=pay_due-x
        sum=ord.total_price+ord.transit_price    
        print(type(delta))
        return render(request, 'df_user/pay.html', locals())



class DeleteadView(LoginRequiredMixin, View):
    def get(self, request,cart_id):
        addr=Address.objects.get(id=cart_id)
        addr.delete()
        return HttpResponseRedirect('/user/address')


class PayRView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        cards =  Card.objects.filter(user=user)
        return  render(request,'df_user//bank.html',locals())

    def post(self, request):
        # 地址添加
        account = request.POST.get('account')

        holder = request.POST.get('holder')
        print(holder)
        dueday= request.POST.get('dueday')
        cvv = request.POST.get('cvv')

        user = request.user

        try:
             card = Card.objects.get(user=user,is_default="1")
        except Card.DoesNotExist:
             card = None  # 不存在默認地址

        if card:
            is_default = False
        else:
            is_default = True

        try:
             cardac = Card.objects.get(account=account)
        except Card.DoesNotExist:
             cardac = None  # 不存在默認地址

        if cardac is not None:
            print("123")
            return HttpResponseRedirect(reverse('user:bank'), {'errmsg': '該卡已存在'})
            
        else:
            Card.objects.create(user=user,
                            account=account,
                            holder=holder,
                            dueday=dueday,
                            cvv=cvv,
                            is_default=is_default)
            print("1234")
            return HttpResponseRedirect(reverse('user:bank'))  # get的請求方式



class BankDeleteadView(LoginRequiredMixin, View):
    def get(self, request,cart_id):
        card=Card.objects.get(id=cart_id)
        
        if card.is_default is True:
            card.delete()
            user = request.user
            card=Card.objects.filter(user=user)
            x=card.first()
            x.is_default=True
            x.save()
       
        else:
            card.delete()
        return HttpResponseRedirect('/user/bank')


class Bankset(LoginRequiredMixin, View):
    def get(self, request,cart_id):
        user = request.user
        card = Card.objects.get(user=user,is_default="1")
        card.is_default=False
        card.save()
        card=Card.objects.get(id=cart_id)
        card.is_default=True
        card.save()
        return HttpResponseRedirect('/user/bank')
           

class GinView(LoginRequiredMixin, View):
    def get(self, request):
        orderid=request.GET.get("order_id")
        order = OrderInfo.objects.select_for_update().get(id=int(orderid))
        skuinfos=OrderDetailinfo.objects.filter(order=order)
        
        return render(request, 'df_user/gin.html', locals())


