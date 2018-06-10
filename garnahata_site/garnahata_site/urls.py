from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.conf.urls import include, url


from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

from garnahata_site.sitemaps import MainXML, NewsXML, StaticXML
from garnahata_site.feeds import LatestNewsFeed
from catalog import views as catalog_views
from catalog.models import Address
from cms_pages import views as cms_pages_views


urlpatterns = [
    url(r'^ajax/suggest$', catalog_views.suggest, name='suggest'),

    url(r'^a/(?P<slug>.+)$', catalog_views.address_details,
        name='address_details'),

    url(r'^tag/', include('cms_pages.urls')),

    url(r'^latest$', catalog_views.latest_addresses,
        name='latest_addresses'),

    url(r'^by_city$', catalog_views.addresses_by_city,
        name='addresses_by_city'),

    url(r'^news$', cms_pages_views.news, name='news'),

    url(r'^news/special$', cms_pages_views.news, name='special_news',
        kwargs={'special': True}),

    url(r'^search$', catalog_views.search, name='search'),

    url(r'^sitemap\.xml$', sitemap, {
        'sitemaps': {
            'main': MainXML,
            'adresses': GenericSitemap({
                'queryset': Address.objects.all(),
                'date_field': "date_added",
            }),
            'news': NewsXML,
            'static': StaticXML,
        }},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^admin/fs/', include('fs.urls')),

    url(r'^search_ownerships$', catalog_views.search,
        name='search_ownerships', kwargs={"sources": ["ownerships"]}),

    url(r'^search_addresses$', catalog_views.search,
        name='search_addresses', kwargs={"sources": ["addresses"]}),

    url(r'^feeds/news/$', LatestNewsFeed(), name="rss_feed"),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
