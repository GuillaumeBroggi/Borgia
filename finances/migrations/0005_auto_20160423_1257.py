# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 10:57
from __future__ import unicode_literals

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0004_auto_20160423_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='cheque_number',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[0-9]{7}$', 'Numéro de chèque invalide')], verbose_name='Numéro de chèque'),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='signature_date',
            field=models.DateField(default=datetime.datetime(2016, 4, 23, 10, 57, 12, 18257, tzinfo=utc), verbose_name='Date de signature'),
        ),
        migrations.AlterField(
            model_name='debitbalance',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='debitbalance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 23, 10, 57, 12, 16715, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='lydia',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='lydia',
            name='date_operation',
            field=models.DateField(default=datetime.datetime(2016, 4, 23, 10, 57, 12, 23788, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 23, 10, 57, 12, 8768, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='sharedevent',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 4, 23, 10, 57, 12, 25632, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='sharedevent',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Prix'),
        ),
    ]
