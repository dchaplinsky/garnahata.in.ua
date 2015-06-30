# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='title',
            field=models.CharField(max_length=150, default='', verbose_name='Коротка адреса'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(blank=True, verbose_name='Адреса'),
            preserve_default=True,
        ),
    ]
