# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0004_auto_20161123_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
    ]
