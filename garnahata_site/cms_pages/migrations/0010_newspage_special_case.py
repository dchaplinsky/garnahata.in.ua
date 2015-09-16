# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0009_auto_20150723_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspage',
            name='special_case',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
