# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20161202_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
