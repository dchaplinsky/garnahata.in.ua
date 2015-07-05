# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20150706_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Адреси', 'verbose_name': 'Адреса'},
        ),
        migrations.AlterModelOptions(
            name='ownership',
            options={'verbose_name_plural': 'Власники', 'verbose_name': 'Власник'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name_plural': "Об'єкти", 'verbose_name': "Об'єкт"},
        ),
    ]
