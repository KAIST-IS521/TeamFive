# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 07:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0003_auto_20170519_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boarduser',
            name='user',
        ),
        migrations.DeleteModel(
            name='BoardUser',
        ),
    ]
