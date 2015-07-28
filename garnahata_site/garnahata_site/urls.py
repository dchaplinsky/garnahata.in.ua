from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls

from catalog.sitemaps import LatestXML, СitiesXML

sitemaps_1 = {
            'latest': LatestXML,
}

sitemaps_2 = {
            'cities': СitiesXML,
}

urlpatterns = patterns(
    '',
    url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),

    url(r'^a/(?P<slug>.+)$', 'catalog.views.address_details',
        name='address_details'),

    #url(r'^a/(?P<slug>.+)/sitemap\.xml$', 
       # 'django.contrib.sitemaps.views.sitemap',
        #{'sitemaps': sitemaps_3}),

    url(r'^tag/', include('cms_pages.urls',namespace="cms_pages")),

    url(r'^latest$', 'catalog.views.latest_addresses',
        name='latest_addresses'),

    url(r'^latest/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps_1}),

    url(r'^by_city$', 'catalog.views.addresses_by_city',
        name='addresses_by_city'),

    url(r'^by_city/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps_2}),

    url(r'^search$', 'catalog.views.search',
        name='search'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
