# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django import VERSION as DJANGO_VERSION


def populate_static_pages(apps, schema_editor):
    RawHTMLPage = apps.get_model('cms_pages.RawHTMLPage')
    ContentType = apps.get_model('contenttypes.ContentType')
    HomePage = apps.get_model('cms_pages.HomePage')
    HomePageTopMenuLink = apps.get_model('cms_pages.HomePageTopMenuLink')

    raw_html_page_content_type, _ = ContentType.objects.get_or_create(
        model='rawhtmlpage',
        app_label='cms_pages',
        defaults={'name': 'rawhtmlpage'} if DJANGO_VERSION < (1, 8) else {}
    )

    home_page = HomePage.objects.all()[0]

    # Create about page
    about_page = RawHTMLPage.objects.create(
        title="Декларації: Про проект",
        slug='about',
        content_type=raw_html_page_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        body="""
<p>Вас вітає проект Канцелярської сотні — «Гарнахата».</p>
        """,
        url_path='/home/about/',
    )

    # Create API page
    api_page = RawHTMLPage.objects.create(
        title="ГарнаХата: Відкритий API",
        slug='api',
        content_type=raw_html_page_content_type,
        path='000100010002',
        depth=3,
        numchild=0,
        body="""
<p>Тут колись буде про наше API</p>
        """,
        url_path='/home/api/',
    )

    HomePageTopMenuLink.objects.create(
        caption="Головна",
        link_external="/",
        sort_order=0,
        page_id=home_page.id
    )

    HomePageTopMenuLink.objects.create(
        caption="Про проект",
        link_page_id=about_page.id,
        sort_order=3,
        page_id=home_page.id
    )

    HomePageTopMenuLink.objects.create(
        caption="Відкритий API",
        link_page_id=api_page.id,
        sort_order=4,
        page_id=home_page.id
    )

    home_page.depth = 2
    home_page.numchild = 2
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_pages', '0002_auto_20150702_0240'),
    ]

    operations = [
        migrations.RunPython(populate_static_pages),
    ]
