# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20150705_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='link',
            field=models.URLField(blank=True, verbose_name='Посилання на сайт забудовника', max_length=1000),
            preserve_default=True,
        ),
    ]
