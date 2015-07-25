from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import patterns, include, url

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = patterns(
    '',
    url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),

    url(r'^a/(?P<slug>.+)$', 'catalog.views.address_details',
        name='address_details'),

    url(r'^tag/(?P<slug>.+)$', 'catalog.views.news_details',
        name='news_details'),

    url(r'^latest$', 'catalog.views.latest_addresses',
        name='latest_addresses'),

    url(r'^by_city$', 'catalog.views.addresses_by_city',
        name='addresses_by_city'),

    url(r'^search$', 'catalog.views.search',
        name='search'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
