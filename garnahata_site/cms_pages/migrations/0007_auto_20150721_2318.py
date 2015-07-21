# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_homepage_url(apps, schema_editor):
    HomePageTopMenuLink = apps.get_model('cms_pages.HomePageTopMenuLink')

    hp_link = HomePageTopMenuLink.objects.get(
        link_external="/#scrollToMe",
    )

    hp_link.link_external = "/#home"
    hp_link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0006_auto_20150720_0217'),
    ]

    operations = [
        migrations.RunPython(fix_homepage_url),
    ]
