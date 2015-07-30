# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20150730_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.IntegerField(choices=[(26, 'Івано-Франківськ'), (5, 'Вінниця'), (12, 'Дніпропетровськ'), (14, 'Донецьк'), (18, 'Житомир'), (23, 'Запоріжжя'), (32, 'Київська область'), (35, 'Кіровоград'), (44, 'Луганськ'), (7, 'Луцьк'), (46, 'Львів'), (48, 'Миколаїв'), (51, 'Одеса'), (53, 'Полтава'), (56, 'Рівне'), (85, 'Севастополь'), (59, 'Суми'), (1, 'Сімферополь'), (61, 'Тернопіль'), (21, 'Ужгород'), (63, 'Харків'), (65, 'Херсон'), (68, 'Хмельницький'), (71, 'Черкаси'), (73, 'Чернівці'), (74, 'Чернігів'), (80, 'м. Київ')], verbose_name='Місто', default=80),
        ),
        migrations.AlterIndexTogether(
            name='ownership',
            index_together=set([('id', 'prop', 'owner')]),
        ),
    ]
