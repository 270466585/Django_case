# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('banner', models.ImageField(upload_to=b'banner')),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=10)),
                ('cover', models.ImageField(upload_to=b'category')),
                ('className', models.CharField(default=b'', max_length=10)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('picture', models.ImageField(upload_to=b'goods')),
                ('unit', models.CharField(default=b'500g', max_length=20)),
                ('click', models.IntegerField(default=0)),
                ('intro', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('content', tinymce.models.HTMLField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('isTop', models.BooleanField(default=False)),
                ('isDelete', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='fruitShop.GoodsCategory')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('number', models.IntegerField(default=0)),
                ('goods', models.ForeignKey(to='fruitShop.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('isPay', models.BooleanField(default=False)),
                ('totalPrice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('address', models.CharField(default=b'', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=0)),
                ('good', models.ForeignKey(to='fruitShop.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(default=b'', max_length=11)),
                ('shou_people', models.CharField(default=b'', max_length=10)),
                ('p_c_a_detail', models.CharField(default=b'', max_length=100)),
                ('zip_code', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='shopcart',
            name='user',
            field=models.ForeignKey(to='fruitShop.UserInfo'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(to='fruitShop.UserInfo'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='fruitShop.OrderInfo'),
        ),
    ]
