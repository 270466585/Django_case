# coding=utf-8
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import *
from decorators import *
from django.db.models import Sum
from django.db import transaction
import datetime
from decimal import Decimal
from haystack.views import SearchView


# 用户注册
def user_register(request):
    if request.method == 'POST':
        # 接受用户输入
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        # 判断两次密码是否相等
        if pwd != cpwd:
            return redirect(reverse('fruitShop:user_register'))
        # 密码加密
        s1 = sha1()
        s1.update(cpwd)
        password = s1.hexdigest()
        # 保存数据
        UserInfo.objects.create(nickname=user_name, password=password, email=email)
    return render(request, 'fruitShop/user/register.html', {'title': '用户注册'})


# 检测用户名时候已存在
def user_exist(request):
    if request.is_ajax():
        nickname = request.GET.get('nickname')
        count = UserInfo.objects.filter(nickname=nickname).count()
        return JsonResponse({'count': count})


# 用户登录
def user_login(request):
    if request.method == 'POST':
        nickname = request.POST.get('username', '')
        password = request.POST.get('pwd', '')
        remember = request.POST.get('remember', 0)
        # 查询用户是否存在
        user = UserInfo.objects.filter(nickname=nickname)
        if len(user) == 1:
            s1 = sha1()
            s1.update(password)
            if s1.hexdigest() == user[0].password:
                # 密码验证成功
                to_url = request.COOKIES.get('to_url', '/')
                redirect = HttpResponseRedirect(to_url)
                if remember:
                    # 记住用户名
                    redirect.set_cookie('nickname', nickname)

                # 保存session用户信息
                request.session['user_id'] = user[0].id
                request.session['nickname'] = nickname
                # 进行跳转
                return redirect
            else:
                context = {'nickname_error': '', 'password_error': '密码错误', 'nickname': nickname, 'pwd': password}
        else:
            context = {'nickname_error': '用户名不存在', 'password_error': '', 'nickname': nickname, 'pwd': password}
        return render(request, 'fruitShop/user/login.html', context)
    nickname = request.COOKIES.get('nickname', '')
    return render(request, 'fruitShop/user/login.html',
                  {'nickname_error': '', 'password_error': '', 'nickname': nickname, 'pwd': '', 'title': '用户登录'})


# 退出登录
def user_logout(request):
    request.session.flush()
    return redirect('/')


# 用户信息
@check_user_login
def user_info(request):
    good_ids = request.COOKIES.get('good_ids', '')
    if good_ids != '':
        good_ids_list = good_ids.split(',')
    else:
        good_ids_list = []
    viewGoods = GoodsInfo.objects.filter(id__in=good_ids_list)
    user_id = request.session.get('user_id', 0)
    user = UserInfo.objects.filter(pk=user_id)
    context = {'userInfo': user[0], 'title': '用户中心-个人信息', 'viewGoods': viewGoods, 'user_p_title': '用户中心'}
    return render(request, 'fruitShop/user/info.html', context)


# 用户订单
@check_user_login
def user_order(request, p):
    if p == '':
        p = 1
    user_id = request.session.get('user_id')
    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-id')
    orderDetails = []
    for order in orders:
        detail = OrderDetail.objects.filter(order_id=order.id)
        order.detail = detail
        orderDetails.append(order)
    print(orderDetails)
    paginator = Paginator(orderDetails, 3)
    page = paginator.page(int(p))
    context = {'title': '用户中心-订单', 'user_p_title': '用户中心', 'page': page, 'p_index': p}
    return render(request, 'fruitShop/user/order.html', context)


# 用户收货地址
@check_user_login
def user_site(request):
    user_id = request.session.get('user_id', 0)
    user = UserInfo.objects.filter(pk=user_id)[0]
    if request.method == 'POST':
        shou_people = request.POST.get('shou_people')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        user.shou_people = shou_people
        user.phone = phone
        user.p_c_a_detail = request.POST.get('address', '')
        if zip_code == '':
            zip_code = 0
        user.zip_code = zip_code
        user.save()
    context = {'title': '用户中心-收货地址', 'userInfo': user, 'user_p_title': '用户中心'}
    return render(request, 'fruitShop/user/site.html', context)


# 首页
def index(request):
    # 所有的分类
    categories = GoodsCategory.objects.all()[:6]
    data = []
    for cate in categories:
        # 根据分类查询商品
        this_good = cate.goodsinfo_set
        if len(this_good.order_by('-click')) > 0:
            data.append({
                'cate': cate,  # 分类
                'goods': this_good.order_by('-click')[:4],  # 分类下的商品
                's_goods': this_good.filter(isTop=1).values('id', 'name')[:4]
            })
    banners = Banner.objects.all()
    context = {'title': '商城首页', 'categories': categories, 'data': data, 'banners': banners}
    return render(request, 'fruitShop/index.html', context)


# 商品列表
def list(request, c_id, p_index, sort):
    cates = __getCategory()
    newGoods = GoodsInfo.objects.filter(category_id=c_id).order_by('-id')[:5]
    if sort == '2':
        sort_by = 'price'
    elif sort == '3':
        sort_by = '-click'
    else:
        sort_by = 'id'
    goods = GoodsInfo.objects.filter(category_id=c_id).order_by(sort_by)
    paginator = Paginator(goods, 30)
    page = paginator.page(int(p_index))
    context = {
        'title': '商品列表',
        'c_id': c_id,
        'sort': sort,
        'page': page,
        'categories': cates,
        'newGoods': newGoods
    }
    return render(request, 'fruitShop/list.html', context)


# 商品详情
def detail(request, id):
    cates = __getCategory()
    good = GoodsInfo.objects.filter(pk=id)[0]
    good.click += 1
    good.save()
    t_goods = GoodsInfo.objects.filter(category_id=good.category_id)[:3]
    cate = GoodsCategory.objects.filter(pk=good.category_id)[0].title
    # 添加商品浏览记录
    good_ids = request.COOKIES.get('good_ids', '')
    good_id = '%d' % good.id
    if good_ids != '':
        good_ids_list = good_ids.split(',')
        # 如果没有就插入一个
        if good_ids_list.count(good_id) == 0:
            good_ids_list.insert(0, good_id)
        if len(good_ids_list) > 5:
            # 删除最后一个
            del good_ids_list[5]
        good_ids = ','.join(good_ids_list)
    else:
        # 添加第一条
        good_ids = good_id
    context = {
        'title': '商品详情',
        'categories': cates,
        'id': id,
        'good': good,
        'cate': cate,
        't_goods': t_goods
    }
    responce = render(request, 'fruitShop/detail.html', context)
    # 保存浏览历史到cookie
    responce.set_cookie('good_ids', good_ids)
    return responce


# 获取分类
def __getCategory():
    categories = GoodsCategory.objects.filter(isDelete=0)
    cates = []
    for cate in categories:
        if len(cate.goodsinfo_set.all()) > 0:
            cates.append(cate)
    return cates


# 购物车
@check_user_login
def cart(request):
    user_id = request.session.get('user_id')
    cartGoods = ShopCart.objects.filter(user_id=user_id)
    context = {'title': '我的购物车', 'cartGoods': cartGoods, 'user_p_title': '我的购物车'}
    return render(request, 'fruitShop/cart.html', context)


# 添加商品到购物车
def addCart(request):
    user_id = request.session.get('user_id', '')
    if user_id == '':
        return JsonResponse({'status': 0, 'msg': '您未登录'})
    else:
        good_id = request.POST.get('id', 0)
        goods_number = GoodsInfo.objects.get(pk=good_id).number
        number = int(request.POST.get('number', 1))
        if goods_number >= number:
            this_goods = ShopCart.objects.filter(good_id=good_id)
            if len(this_goods) == 1:
                this_good = this_goods[0]
                this_good.number += number
                this_good.save()
            else:
                ShopCart.objects.create(user_id=user_id, number=1, good_id=good_id)
            return JsonResponse({'status': 1, 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 3, 'msg': '库存不足'})


# 获取购物车数量
def getMyCartCount(request):
    user_id = request.session.get('user_id', '')
    if user_id == '':
        return JsonResponse({'count': 0})
    else:
        count = ShopCart.objects.filter(user_id=user_id).aggregate(Sum('number'))
        return JsonResponse({'count': count['number__sum']})


# 编辑购物车
@check_user_login
def editCartGood(request):
    id = request.POST.get('id', 0)
    if request.POST.get('delete', 0) == '1':
        this_chart_good = ShopCart.objects.get(pk=id)
        this_chart_good.delete()
        return JsonResponse({'status': 1, 'msg': '删除完成'})
    if request.POST.get('number', 0) != 0:
        number = request.POST.get('number', 0)
        this_chart_good = ShopCart.objects.get(pk=id)
        this_chart_good.number = number
        this_chart_good.save()
        return JsonResponse({'status': 1, 'msg': '修改完成'})


# 预览订单
@check_user_login
def reviewOrder(request):
    address = UserInfo.objects.get(pk=request.session.get('user_id')).p_c_a_detail
    context = {'address': address, 'title': '确认订单', 'user_p_title': '确认订单'}
    cart_ids = request.GET.getlist('selectme')
    carts = ShopCart.objects.filter(id__in=cart_ids)
    context['carts'] = carts
    context['cart_ids'] = '_'.join(cart_ids)
    return render(request, 'fruitShop/review_order.html', context)


# 启用数据库事务操作
@transaction.atomic()
@check_user_login
def orderHandle(request):
    # 记录当前操作点
    tran_id = transaction.savepoint()
    # /接受要支付的购物车id
    cart_ids = request.GET.get('cart_ids')
    try:
        order = OrderInfo()
        now = datetime.datetime.now()
        uid = request.session.get('user_id')
        # 订单id订单号是当前时间加上用户id
        order.id = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.date = now
        totalPrice = 0
        # 记录收货地址
        order.address = UserInfo.objects.get(pk=request.session.get('user_id')).p_c_a_detail
        # 开始计算总价
        cart_ids = cart_ids.split('_')
        for c_id in cart_ids:
            cart = ShopCart.objects.get(pk=int(c_id))
            thisPrice = Decimal(cart.good.price * cart.number)
            totalPrice += thisPrice
        # 加上10快邮费
        order.totalPrice = totalPrice + 10
        order.save()  # 保存订单
        # 开始记录订单详情表
        for c_id in cart_ids:
            # 获取当前购物车id
            cart = ShopCart.objects.get(pk=int(c_id))
            detail = OrderDetail()
            detail.order = order
            good = cart.good
            if good.number >= cart.number:
                # 如果库存大于等于要购买的数量
                good.number -= cart.number
                # 保存商品数量
                good.save()
                detail.goods_id = good.id
                detail.price = good.price
                detail.number = cart.number
                detail.save()
                # 删除购物车
                cart.delete()
            else:
                # 商品不够卖的,返回购物车
                transaction.savepoint_rollback(tran_id)
                return redirect(reverse('fruitShop:cart'))
        # 提交事务
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('=============>%s' % e)
        # 返回
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order/1')


# 假装支付
def pay(request, order_id):
    order = OrderInfo.objects.get(id=int(order_id))
    order.isPay = True
    order.save()
    return redirect('/user/order/1')


# 自定义搜索上下文,传递公共数据
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        categories = GoodsCategory.objects.filter(isDelete=0)
        cates = []
        for cate in categories:
            if len(cate.goodsinfo_set.all()) > 0:
                cates.append(cate)
        context['categories'] = cates
        return context
