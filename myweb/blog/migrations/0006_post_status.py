# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170330_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[(0, '\u5f85\u5ba1\u6838'), (1, '\u5f85\u53d1\u5e03'), (2, '\u5df2\u53d1\u5e03'), (3, '\u672a\u901a\u8fc7\u5ba1\u6838')], default=0, max_length=15, verbose_name='\u53d1\u5e03\u72b6\u6001'),
        ),
    ]
