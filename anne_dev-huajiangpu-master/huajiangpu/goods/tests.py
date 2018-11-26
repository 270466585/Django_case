from django.test import TestCase
from .models import *

# Create your tests here.

# for name in ['鲜花','花束','花篮','婚车','手捧花','展台']:
#     c = Category()
#     c.cate_name = name
#     c.cate_desc = name + '的描述'
#     c.cate_image = 'images/test.jpg'
#     c.save()

# g = Goods()
# g.g_name = '牵牛花'
# g.g_cate_id = 1
# g.g_desc = '青青柔蔓绕修篁，刷翠成花着处芳。应是折从河鼓手，天孙斜插鬓云香。'
# g.g_detail = '牵牛花的花期在秋季；圆叶牵牛花型较小，裂叶牵牛花型稍大；花色为纯色。矮牵牛的花期长达数月（5～7月），花冠喇叭状；花形有单瓣、重瓣、瓣缘皱褶或呈不规则锯齿等; 花色有红、白、粉、紫及各种带斑点、网纹、条纹等'
# g.g_florid = '牵牛花的花语：名誉/爱情永固'
# g.g_image = 'images/goods_test.jpg'
# g.g_price = 2.00
# g.save()


# l = [{'name': '台花', 'cate':6},
#  {'name': '春日', 'cate': 6},
#  {'name': '风信子', 'cate': 1},
#  {'name': '蝴蝶花', 'cate': 2},
#  {'name': '缤纷', 'cate': 2},
# {'name': '欢乐颂', 'cate':3},
#  {'name': '浪漫', 'cate': 3},
#  {'name': '爱情', 'cate': 2},
#  {'name': '太阳花', 'cate': 1}]
# for index, temp in enumerate(l):
#     g = Goods()
#     g.g_name = temp['name']
#     g.g_cate_id = temp['cate']
#     g.g_desc = '青青柔蔓绕修篁，刷翠成花着处芳。应是折从河鼓手，天孙斜插鬓云香。'
#     g.g_detail = '牵牛的花期长达数月（5～7月），花冠喇叭状；花形有单瓣、重瓣、瓣缘皱褶或呈不规则锯齿等; 花色有红、白、粉、紫及各种带'
#     g.g_florid = '牵牛花的花语：名誉/爱情永固'
#     g.g_image = 'images/'+str(index+2)+'.jpg'
#     g.g_price = 2.00
#     g.save()





