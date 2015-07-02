# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def fill_homepage(apps, schema_editor):
    HomePage = apps.get_model('cms_pages.HomePage')
    home_page = HomePage.objects.all()[0]
    home_page.body = """
Канцелярська сотня щаслива представити вам базу даних власників найдорожчої нерухомості України.
Це офіційні дані на основі державного реєстру речових прав. Сподіваємось, що ця інформація допоможе у журналістських розслідуваннях.
""".strip()
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0003_auto_20150702_0241'),
    ]

    operations = [
        migrations.RunPython(fill_homepage),
    ]
