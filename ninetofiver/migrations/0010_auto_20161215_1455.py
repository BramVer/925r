# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 14:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ninetofiver', '0009_auto_20161215_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentcontract',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ninetofiver.Company'),
        ),
        migrations.AlterField(
            model_name='employmentcontract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
