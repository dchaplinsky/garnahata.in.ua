# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0010_newspage_special_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='special_case',
            field=models.BooleanField(db_index=True, verbose_name='Особливий випадок', default=False),
        ),
    ]
