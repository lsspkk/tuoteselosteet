# -*- coding: UTF-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from locale import *
from django.utils.translation import ugettext_lazy as _

# Create your models here.



# Yritys näkee vain omat tuotteensa
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, blank=True, verbose_name = _('user'))
    name = models.CharField(_('Company|name'), max_length=100 )
    description = models.CharField(max_length=1000, blank=True, verbose_name = _('description'))
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')

# Ravintoaineet
class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name = _('Food|name'))
    nameSV = models.CharField(max_length=100, verbose_name = _('Food|nameSV'))
    description = models.CharField(max_length=1000, blank=True, verbose_name = _('food|description'))
    descriptionSV = models.CharField(max_length=1000, blank=True, verbose_name = _('food|descriptionSV'))
    link = models.CharField(max_length=1000, blank=True, verbose_name = _('link'))
    extra = models.CharField(max_length=1000, blank=True, verbose_name = _('extra'))
    energy = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('energy'))
    fat = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('fat'))
    saturatedFat = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('saturatedFat'))
    carbohydrate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('carbohydrate'))
    sugar = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('sugar'))
    fiber = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('fiber'))
    protein = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('protein'))
    salt = models.DecimalField(default=0, max_digits=12, decimal_places=10, verbose_name = _('salt'))
    def __str__(self):
        if self.description in [None, '']:
            return self.name
        else:
            return "%s[%s]" % ( self.name , (self.description[0:10] + "..."))
    def __unicode__(self):
        if self.description in [None, '']:
            return self.name
        else:
            return "%s[%s]" % ( self.name , (self.description[0:10] + "..."))
    class Meta:
        verbose_name = _('food')
        verbose_name_plural = _('foods')

# Tuote laskee ravintoarvonsa
class Product(models.Model):
    name = models.CharField(verbose_name = _('Product|name'), max_length=100)
    nameSV = models.CharField(verbose_name = _('Product|nameSV'), max_length=100)
    ingredients = models.ManyToManyField(Food, through='Amount', related_name="sisus")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1, verbose_name = _('company'))
    weight = models.IntegerField(default=0, blank=True,  verbose_name = _('weight'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
    def get_total_weight(self):
        w = 0
        for a in self.amount_set.all():
            w += a.weight
        return w

    def get_nutrition_facts(self):
        w = self.get_total_weight();
        r = { 'energia1' : 0.0 ,
              'energia2' : 0.0,
              'rasva' : 0.0,
              'tyydyttynyt' : 0.0,
              'hiilihydraatti' : 0.0,
              'sokeri' : 0.0,
              'ravintokuitu' : 0.0,
              'proteiini' : 0.0,
              'suola' : 0.0
               }
        for a in self.amount_set.all():
            p = a.weight / w #procent
            r['energia1'] += float(a.food.energy) * p
            r['energia2'] += float(a.food.energy) * p / 4.184
            r['rasva'] += float(a.food.fat) * p
            r['tyydyttynyt'] += p * float(a.food.saturatedFat)
            r['hiilihydraatti'] += p * float(a.food.carbohydrate)
            r['sokeri'] += p * float(a.food.sugar)
            r['ravintokuitu'] += p * float(a.food.fiber)
            r['proteiini'] += p * float(a.food.protein)
            r['suola'] += p * float(a.food.salt)

        return r

# kuinka paljon mitäkin raaka-ainetta on reseptissä
class Amount(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name = _('food'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField(_('weight'), default=0)
    def __str__(self):
            return "%s, %s g" % (self.food.name, self.weight)
    def __unicode__(self):
            return "%s, %s g" % (self.food.name, self.weight)
    class Meta:
        verbose_name = _('amount')
        verbose_name_plural = _('amounts')
        ordering = ('-weight',)

# Allergian aiheuttajat
class Allergen(models.Model):
    name = models.CharField(max_length=100, verbose_name = _('Allergen|name'))
    nameSV = models.CharField(max_length=100, blank = True, verbose_name = _('Allergen|nameSV'))
    class Meta:
        verbose_name = _('allergen')
        verbose_name_plural = _('allergens')
