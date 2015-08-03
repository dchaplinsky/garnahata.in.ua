# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20150731_0127'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='address',
            index_together=set([('id', 'city', 'title')]),
        ),
    ]
