# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_address_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.IntegerField(choices=[(1, 'Сімферополь'), (71, 'Черкаси'), (68, 'Хмельницький'), (5, 'Вінниця'), (65, 'Херсон'), (73, 'Чернівці'), (74, 'Чернігів'), (12, 'Дніпропетровськ'), (14, 'Донецьк'), (80, 'Київ'), (18, 'Житомир'), (21, 'Ужгород'), (23, 'Запоріжжя'), (26, 'Івано-Франківськ'), (32, 'Київ'), (35, 'Кіровоград'), (7, 'Луцьк'), (44, 'Луганськ'), (46, 'Львів'), (48, 'Миколаїв'), (51, 'Одеса'), (53, 'Полтава'), (56, 'Рівне'), (59, 'Суми'), (61, 'Тернопіль'), (85, 'Севастополь'), (63, 'Харків')], default=80, verbose_name='Місто'),
        ),
    ]
