# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 12:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=255)),
                ('internal', models.BooleanField(default=False)),
                ('vat_identification_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid VAT identification number', regex='^\\d{2}[a-z0-9]{2,13}$')])),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ninetofiver.company_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'companies',
                'abstract': False,
            },
        ),
    ]