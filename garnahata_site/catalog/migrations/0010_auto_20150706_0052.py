# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20150706_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='link',
            field=models.URLField(db_index=True, verbose_name='Посилання на сайт забудовника', blank=True, max_length=1000),
            preserve_default=True,
        ),
    ]
