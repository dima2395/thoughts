# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20161202_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(default='/avatars/default-avatar.png', upload_to='avatars'),
        ),
    ]
