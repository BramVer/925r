# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-31 10:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninetofiver', '0037_userinfo_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='join_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Became Inuit on'),
        ),
    ]
