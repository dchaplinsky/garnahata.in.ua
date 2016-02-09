# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20150916_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='meta_description',
            field=models.TextField(blank=True, default='', verbose_name='meta description сторінки'),
        ),
        migrations.AddField(
            model_name='address',
            name='meta_title',
            field=models.CharField(blank=True, max_length=150, verbose_name='title сторінки', default=''),
        ),
    ]
