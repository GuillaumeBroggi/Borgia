# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 16:30
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Prix d'achat")),
                ('purchase_date', models.DateField(default=django.utils.timezone.now, verbose_name="Date d'achat")),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name="Date d'expiration")),
                ('place', models.CharField(max_length=255, verbose_name='Lieu de stockage')),
                ('quantity_remaining', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Quantité d'unité produit restante")),
                ('is_sold', models.BooleanField(default=False, verbose_name='Est vendu')),
            ],
            options={
                'permissions': (('list_container', 'Lister les conteneurs'), ('retrieve_container', 'Afficher un conteneur'), ('change_active_keg', "Changer le fut d'une tireuse")),
            },
        ),
        migrations.CreateModel(
            name='ProductBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Product base name', max_length=255, verbose_name='Nom')),
                ('description', models.TextField(default='Description', verbose_name='Description')),
                ('is_manual', models.BooleanField(default=False, verbose_name='Gestion manuelle du prix')),
                ('manual_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Prix manuel')),
                ('brand', models.CharField(max_length=255, verbose_name='Marque')),
                ('type', models.CharField(choices=[('single_product', 'Produit unitaire'), ('container', 'Conteneur')], default='single_product', max_length=255, verbose_name='Type')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Quantité d'unité de produit")),
            ],
            options={
                'permissions': (('list_productbase', 'Lister les produits de base'), ('retrieve_productbase', 'Afficher un produit de base'), ('change_price_productbase', "Changer le prix d'un produit de base")),
            },
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Product unit name', max_length=255, verbose_name='Nom')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('unit', models.CharField(choices=[('CL', 'cl'), ('G', 'g'), ('CENT', 'cent')], default='CL', max_length=255, verbose_name='Unité')),
                ('type', models.CharField(choices=[('keg', 'fut'), ('liquor', 'alcool fort'), ('syrup', 'sirop'), ('soft', 'soft'), ('food', 'alimentaire'), ('meat', 'viande'), ('cheese', 'fromage'), ('side', 'accompagnement'), ('fictional_money', 'argent fictif')], default='keg', max_length=255, verbose_name='Type')),
            ],
            options={
                'permissions': (('list_productunit', 'Lister les unités de produits'), ('retrieve_productunit', 'Afficher une unité de produit')),
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Shop name', max_length=255, verbose_name='Nom')),
                ('description', models.TextField(default='Description', verbose_name='Description')),
            ],
            options={
                'permissions': (('reach_workboard_foyer', 'Aller sur le workboard du foyer'), ('reach_workboard_auberge', "Aller sur le workboard de l'auberge"), ('sell_auberge', "Vendre des produits à l'auberge")),
            },
        ),
        migrations.CreateModel(
            name='SingleProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Prix d'achat")),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Prix de vente')),
                ('purchase_date', models.DateField(default=django.utils.timezone.now, verbose_name="Date d'achat")),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name="Date d'expiration")),
                ('place', models.CharField(max_length=255, verbose_name='Lieu de stockage')),
                ('is_sold', models.BooleanField(default=False, verbose_name='Est vendu')),
                ('product_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_base_single_product', to='shops.ProductBase')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finances.Sale')),
            ],
            options={
                'permissions': (('list_singleproduct', 'Lister les produits unitaires'), ('retrieve_singleproduct', 'Afficher un produit unitaire')),
            },
        ),
        migrations.CreateModel(
            name='SingleProductFromContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Quantité d'unité de produit")),
                ('sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Prix de vente')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Container')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finances.Sale')),
            ],
        ),
        migrations.AddField(
            model_name='productbase',
            name='product_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_unit', to='shops.ProductUnit'),
        ),
        migrations.AddField(
            model_name='productbase',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Shop'),
        ),
        migrations.AddField(
            model_name='container',
            name='product_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_base_container', to='shops.ProductBase'),
        ),
    ]
