# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selosteet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Allergen|name')),
                ('nameSV', models.CharField(blank=True, max_length=100, verbose_name='Allergen|nameSV')),
            ],
            options={
                'verbose_name': 'allergen',
                'verbose_name_plural': 'allergens',
            },
        ),
    ]