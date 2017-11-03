# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 08:14
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
            ],
            options={
                'permissions': (('list_inventory', 'Lister les inventaires de stock'), ('retrieve_inventory', 'Afficher les inventaires de stock')),
            },
        ),
        migrations.CreateModel(
            name='InventoryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
            ],
            options={
                'permissions': (('list_stockentry', 'Lister les entrées de stock'), ('retrieve_stockentry', 'Afficher les entrées de stock')),
            },
        ),
        migrations.CreateModel(
            name='StockEntryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Prix')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Product')),
                ('stockentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.StockEntry')),
            ],
        ),
    ]
