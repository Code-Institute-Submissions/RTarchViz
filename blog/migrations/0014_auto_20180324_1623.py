# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20180321_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=3000),
        ),
    ]
