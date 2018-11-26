# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='hostshmodify',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('IP', models.CharField(max_length=56)),
                ('username', models.CharField(max_length=56)),
                ('password', models.CharField(max_length=128)),
                ('onegroup', models.CharField(max_length=256)),
                ('twogroup', models.CharField(max_length=256)),
                ('reductionone', models.CharField(max_length=256)),
                ('reductiontwo', models.CharField(max_length=256)),
                ('Remark', models.TextField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='jenkinsmodify',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=56)),
                ('password', models.CharField(max_length=128)),
                ('UrlLocation', models.CharField(max_length=128)),
                ('Remark', models.TextField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='lvsmodify',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=56)),
                ('password', models.CharField(max_length=128)),
                ('IP', models.CharField(max_length=56)),
                ('ScriptLocation', models.CharField(max_length=128)),
                ('onegroup', models.CharField(max_length=256)),
                ('twogroup', models.CharField(max_length=256)),
                ('Remark', models.TextField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='publishmodify',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('onegroup', models.CharField(max_length=256)),
                ('twogroup', models.CharField(max_length=256)),
                ('Remark', models.TextField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('release', models.CharField(max_length=128)),
                ('type_list', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u53d1\u5e03\u8bb0\u5f55',
                'verbose_name_plural': '\u53d1\u5e03\u8bb0\u5f55',
            },
        ),
    ]
