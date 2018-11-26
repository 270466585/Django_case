# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lvsmodify',
            name='IntranetIP',
            field=models.CharField(default=datetime.datetime(2017, 2, 22, 12, 17, 40, 194000), max_length=56),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lvsmodify',
            name='Intranetonegroup',
            field=models.CharField(default=datetime.datetime(2017, 2, 22, 12, 17, 43, 936000), max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lvsmodify',
            name='Intranettwogroup',
            field=models.CharField(default=datetime.datetime(2017, 2, 22, 12, 17, 47, 662000), max_length=256),
            preserve_default=False,
        ),
    ]
