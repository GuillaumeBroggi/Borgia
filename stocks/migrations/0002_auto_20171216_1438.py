# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-16 13:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockentry',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='products',
            field=models.ManyToManyField(through='stocks.StockEntryProduct', to='shops.Product'),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Shop'),
        ),
        migrations.AddField(
            model_name='inventoryproduct',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Inventory'),
        ),
        migrations.AddField(
            model_name='inventoryproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Product'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='products',
            field=models.ManyToManyField(through='stocks.InventoryProduct', to='shops.Product'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Shop'),
        ),
    ]
