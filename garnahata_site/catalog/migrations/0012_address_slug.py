# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20150706_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='slug',
            field=models.SlugField(default='', max_length=200, verbose_name='slug'),
            preserve_default=False,
        ),
    ]
