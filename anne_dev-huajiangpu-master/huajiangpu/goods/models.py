from db.AbstractModel import BaseModel
from django.db import models


class Category(BaseModel):
    cate_name = models.CharField(max_length=20)
    cate_image = models.ImageField()
    cate_desc = models.CharField(max_length=500)

    def __str__(self):
        return self.cate_name


class GoodsManager(models.Manager):
    def goods_by_hot(self):
        return self.all().order_by('g_look')[:10]

    def goods_by_cate(self, cate_id):
        return self.filter(g_cate_id=cate_id)

    def goods_by_id(self, goods_id):
        try:
            return self.get(pk=goods_id)
        except Goods.DoesNotExist:
            return None


class Goods(BaseModel):
    # 名字，
    g_name = models.CharField(max_length=30)
    # 类别，
    g_cate = models.ForeignKey(Category)
    # 单位，
    g_unit = models.CharField(max_length=10)
    # 价格，
    g_price = models.DecimalField(max_digits=10, decimal_places=2)
    # 人气，
    g_look = models.IntegerField(default=0)
    # 描述，
    g_desc = models.CharField(max_length=100)
    # 详情，
    g_detail = models.CharField(max_length=500)
    # 主图，
    g_image = models.ImageField()
    # 细节图，
    g_images = models.CharField(max_length=500)
    # 花语
    g_florid = models.CharField(max_length=100)

    objects = GoodsManager()

    def __str__(self):
        return self.g_name


class AdvertisingManager(models.Manager):
    def adv_by_id(self, adv_id):
        try:
            return self.get(pk=adv_id)
        except Advertising.DoesNotExist:
            return None


class Advertising(BaseModel):
    # 标题
    adv_title = models.CharField(max_length=50)
    # 副标题
    adv_subtitle = models.CharField(max_length=200)
    # 详情
    adv_detail = models.CharField(max_length=500)
    # 图1（525*900）
    adv_image1 = models.ImageField()
    # 图2（1413*900）
    adv_image2 = models.ImageField()
    # 图3（1772*900）
    adv_image3 = models.ImageField()

    objects = AdvertisingManager()

    def __str__(self):
        return self.adv_title

