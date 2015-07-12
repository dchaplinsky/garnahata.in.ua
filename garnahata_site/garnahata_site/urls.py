from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = patterns(
    '',
    url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),
    url(r'^map_markers$', 'catalog.views.map_markers', name='map_markers'),
    (r'^base$', TemplateView.as_view(template_name='base.jinja')),
    # url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),

    # url(r'^search$', 'catalog.views.search', name='search'),
    # url(r'^declaration/(?P<declaration_id>\d+)$', 'catalog.views.details',
    #     name='details'),

    # url(r'^region$', 'catalog.views.regions_home', name='regions_home',),
    # url(r'^office$', 'catalog.views.offices_home', name='offices_home',),

    # # Please maintain that order
    # url(r'^region/(?P<region_name>[^\/]+)/(?P<office_name>.+)$',
    #     'catalog.views.region_office', name='region_office'),
    # url(r'^region/(?P<region_name>.+)$', 'catalog.views.region',
    #     name='region'),

    # url(r'^office/(?P<office_name>.+)$', 'catalog.views.office',
    #     name='office'),

    # url(r'^sitemap.xml$', 'catalog.views.sitemap',
    #     name='sitemap'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
