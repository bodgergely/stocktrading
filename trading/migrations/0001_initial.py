# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('stock_symbol', models.CharField(max_length=20)),
                ('quantity', models.CharField(max_length=20)),
                ('purchase_price', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email_address', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('balance', models.CharField(max_length=20)),
            ],
        ),
    ]
