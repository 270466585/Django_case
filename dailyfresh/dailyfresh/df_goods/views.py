# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator, Page


def index(request):
    """查询各分类中的 最新四条数据和最热4条数据"""
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title':'首页','guest_cart':1,
               'type0':type0,'type01':type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               }
    return render(request,'df_goods/index.html',context)


def list(request,tid,pindex,sort):
    """商品列表页 tid是类型编号typeid pindex是页码 sort 是排序依据"""
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort=="1":  # 默认排序

        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == "2":  # 价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == "3": # 热度 点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # 分页
    paginator = Paginator(goods_list,10)
    page = paginator.page(int(pindex))
    context = {
        'title':typeinfo.ttitle,'guest_cart':1,
        'page':page,
        'paginator':paginator,
        'typeinfo':typeinfo,
        'goods_list':goods_list,
        'sort':sort,
        'news':news
    }
    return render(request,'df_goods/list.html',context)


def detail(request,id):
    """商品详情"""
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title':goods.gtype.ttitle,'guest_chart':1,
        'goods':goods,'news':news,'id':id
    }
    return render(request,'df_goods/detail.html',context)
    # reponse = render(request,'df_goods/detail.html',context)

    # 记录最近浏览记录，在用户中心使用
    # goods_id = request.COOKIES.get('goods_ids','')
    # goods_id = "%d" % goods_id
    # if goods_id != '':
    #     goods_ids1 = goods_id.split(',')  # 拆分成列表
    #     if goods_ids1 .count(goods_id) >= 1:  # 如果商品已经被记录，删除-》重新添加
    #         goods_ids1.remove(goods_id)
    #     goods_ids1.insert(0,goods_id)
    #     if len(goods_ids1) >= 6:  # 只维护 展示五个数据
    #         del goods_ids1[5]
    #     goods_ids = ','.join(goods_ids1)  # 拼接成字符串
    # else:
    #     goods_ids =goods_id  # 如果记录为空直接添加
    # reponse.set_cookie('goods_ids',goods_ids)  # 写cookie
    #
    # return reponse
